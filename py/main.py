# main page rss driver

import logging
import json
import jinja2
import os
import webapp2
from google.appengine.api import users
import page_rss

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/../templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class SplashHandler(webapp2.RequestHandler):
  def get(self):
    # TODO The splash handler is not very welcoming right now.
    self.redirect('/feeds')
    # self.response.headers['Content-Type'] = 'text/html'
    # template = JINJA_ENV.get_template('splash.html')
    # self.response.write(template.render({}))

class FeedsHandler(webapp2.RequestHandler):
  def get(self, **kwargs):
    self.handle()
  def post(self, **kwargs):
    data = {}
    if self.request.get('action') == 'edit':
      data['loaded_feed'] = page_rss.GetFeed(self.request.get('feed_id'))
    elif self.request.get('action') == 'test':
      data['test_data'] = page_rss.GetTestData(
          self.request.get('url'),
          self.request.get('xpath'))
      data['loaded_feed'] = self.request.POST
    elif self.request.get('action') == 'delete':
      page_rss.DeleteFeed(
          users.get_current_user().nickname(),
          self.request.get('feed_id'))
    elif self.request.get('action') == 'save':
      page_rss.SaveFeed(
          users.get_current_user().nickname(),
          self.request.get('feed_id'),
          self.request.get('title'),
          self.request.get('url'),
          self.request.get('xpath'))
      data['loaded_feed'] = self.request.POST
    self.handle(**data)
  def handle(
      self, test_data=None, save_data=None, loaded_feed=None, message=None):
    feeds = page_rss.GetFeedsForUser(users.get_current_user().nickname())
    self.response.headers['Content-Type'] = 'text/html'
    template = JINJA_ENV.get_template('feeds.html')
    self.response.write(template.render({
      'feeds': feeds,
      'test_data': test_data,
      'save_data': save_data,
      'loaded_feed': loaded_feed,
      'message': message,
    }))

class RSSHandler(webapp2.RequestHandler):
  def get(self, **kwargs):
    rss_data = page_rss.GetRssData(kwargs['feed_id'])
    self.response.headers['Content-Type'] = 'application/atom+xml'
    template = JINJA_ENV.get_template('rss.xml')
    self.response.write(template.render({
      'rss_data': rss_data,
    }))

application = webapp2.WSGIApplication([
  webapp2.Route('/', handler=SplashHandler),
  webapp2.Route('/feeds', handler=FeedsHandler),
  webapp2.Route('/rss/<feed_id>', handler=RSSHandler),
], debug=True)

