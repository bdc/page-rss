# page_rss module

import datetime
from google.appengine.api import app_identity
import logging
import re
import urllib2
from lxml import etree
from models import feed
from models import feed_item



SETTINGS = {
  'stale_page_seconds': 10*1,  # if our data is older than this, scrape the url
}


def _ElementToText(element):
  text = etree.tostring(element, method='text')
  text = re.sub('[^a-zA-Z\d\-_ \.!\?]', '', text)
  return text

def _Scrape(url, xpath):
  logging.info('Scraping %s...', url)
  try:
    url_req = urllib2.Request(url, headers={'User-Agent': 'Page-RSS'})
    page = urllib2.urlopen(url_req)
  except urllib2.HTTPError as e:
    return [
      {'text': 'Unfortunately, this page will not let you scrape.'},
      {'text': e},
    ] 
  except ValueError:
    return [
      {'text': 'You have not typed a valid url.'},
    ] 
  page_html = etree.parse(page, etree.HTMLParser())
  elements = page_html.xpath(xpath)
  return elements

def _FormatTime(dt):
  dt_rounded = dt.replace(microsecond=0)
  return '%sZ' % dt_rounded.isoformat('T')

def GetFeedsForUser(user_id):
  feeds = feed.Feed.query(feed.Feed.user_id == user_id).order(feed.Feed.title)
  logging.info(feeds)
  rsp = []
  for feed_obj in feeds:
    rsp.append({
      'feed_id': feed_obj.key.id(),
      'title': feed_obj.title,
      'url': feed_obj.url,
      'xpath': feed_obj.xpath,
    })
  return rsp

def GetTestData(url, xpath):
  elements = _Scrape(url, xpath)
  rsp = []
  for element in elements:
    rsp.append({
      'text': _ElementToText(element)
    })
  return rsp

def GetRssData(feed_id):
  feed_obj = feed.Feed.safe_get(feed_id)
  if not feed_obj:
    return None  # no such feed
  if (datetime.datetime.now() - feed_obj.updated_time >
      datetime.timedelta(seconds=SETTINGS['stale_page_seconds'])):
    old_elements = feed_item.FeedItem.query(ancestor=feed_obj.key)
    new_elements = _Scrape(feed_obj.url, feed_obj.xpath)
    elements_to_del = {}
    elements_to_add = {}
    for new_element in new_elements:
      elements_to_add[_ElementToText(new_element)] = new_element
    for old_element in old_elements:
      elements_to_del[old_element.text] = old_element
    both = set(elements_to_add.keys()).intersection(set(elements_to_del.keys()))
    for key in both:
      del elements_to_add[key]
      del elements_to_del[key]
    for key in elements_to_del:
      elements_to_del[key].key.delete()
    for key in elements_to_add:
      feed_item_obj = feed_item.FeedItem(parent=feed_obj.key, text=key)
      feed_item_obj.put()
    feed_obj.updated_time = datetime.datetime.now()
    feed_obj.put()
  feed_items = feed_item.FeedItem.query(ancestor=feed_obj.key)
  rsp = {
    'feed_id': feed_obj.key.id(),
    'title': feed_obj.title,
    'url': feed_obj.url,
    'rss_url': 'http://%s/rss/%s' % (
        app_identity.get_default_version_hostname(), feed_obj.key.id()),
    'updated_time': feed_obj.updated_time.isoformat('T'),
    'updated_time': _FormatTime(feed_obj.updated_time),
    'feed_items': [],
  }
  for feed_item_obj in feed_items:
    rsp['feed_items'].append({
      'text': feed_item_obj.text,
      'item_id': '%s/item/%s' % (rsp['rss_url'], feed_item_obj.key.id()),
      'updated_time': _FormatTime(feed_item_obj.updated_time),
    })
  return rsp

def DeleteFeed(user_id, feed_id):
  feed_obj = feed.Feed.safe_get(feed_id)
  if not feed_obj:
    return  # nothing to delete
  if user_id != feed_obj.user_id:
    return  # not owner, can't delete
  feed_obj.key.delete()

def GetFeed(feed_id):
  feed_obj = feed.Feed.safe_get(feed_id)
  if not feed_obj:
    return None  # nothing to get
  rsp = {
    'feed_id': feed_id,
    'title': feed_obj.title,
    'url': feed_obj.url,
    'xpath': feed_obj.xpath,
  }
  return rsp

def SaveFeed(user_id, feed_id, title, url, xpath):
  if not user_id or not title or not url or not xpath:
    return None  # missing required data, can't save
  feed_obj = feed.Feed.safe_get(feed_id)
  if not feed_obj:
    feed_obj = feed.Feed(title=title, url=url, xpath=xpath, user_id=user_id)
  elif user_id != feed_obj.user_id:
    return None  # not owner, can't save
  feed_obj.title = title
  feed_obj.url = url
  feed_obj.xpath = xpath
  feed_obj.put()
  return feed_obj.key.id()


