Page-RSS
========

What it do, yo
--------------
Page RSS turns any webpage into an RSS feed. It doesn't need to be your own. All you need is a URL and an xpath expression.

Why use, brah
-------------
If you already use an RSS reader, use it to get notified when a webpage gets updated without having to visit it periodically, for instance, or subscribe to something that doesn't have a built-in subscription system. You could use it to see when your favorite TV show has an update, or when a friend's wedding registry gets posted. If you don't use an RSS reader, you could pipe it into something like Zapier or IFTTT.

What I can't?
-------------
If the page you want to track requires a log in, or is a web app with lots of dynamic content, this tool isn't going to be able to do it for ya. Sorry.

I dig it.
---------
Ya.

Where it be?
------------
The prototype is running in appengine at [http://page-rss.appspot.com](http://page-rss.appspot.com).

Do I need to know xpath?
------------------------
Well, yes, that's the idea. You could always [Google it](https://www.google.com/search?q=xpath) to get a refresher on the syntax.

Why am I being prompted to log in?
----------------------------------
You're asked to log in so that your entries don't collide with other users. That way, you can't modify or delete their entries, and they can't mess with yours. You can still read other people's feeds though, if they tell you the feed's rss url. Only your Google username is read for this purpose, and never shared or published.

Next updates
------------
* Bug with most recently saved item not immediately appearing in the 'Existing' list
* Add a few 'default' feeds so new users can play with examples
* Add explanation text to 'About'
* Make it Ajaxy
* Add a splash page
* Pretty UI
* More configurable options for how feed appears

