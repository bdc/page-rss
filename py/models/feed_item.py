from google.appengine.ext import ndb

class FeedItem(ndb.Model):
  text = ndb.StringProperty()
  updated_time = ndb.DateTimeProperty(auto_now_add=True)


