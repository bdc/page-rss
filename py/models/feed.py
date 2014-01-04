from google.appengine.ext import ndb

class Feed(ndb.Model):
  title = ndb.StringProperty(required=True)
  url = ndb.StringProperty(required=True)
  xpath = ndb.StringProperty(required=True)
  user_id = ndb.StringProperty()
  created_time = ndb.DateTimeProperty(auto_now_add=True)
  updated_time = ndb.DateTimeProperty(auto_now_add=True)

  @staticmethod
  def safe_get(feed_id):
    if not feed_id:
      return None
    return Feed.get_by_id(long(feed_id))


