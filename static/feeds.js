// Javascript module for managing feeds.

_AJAX = false;  // For when Ajax is implemented.

testFeed = (function() {
  return _AJAX?
  function() {
    alert('Ajax function');
  }:
  function() {
    document.forms[0].action.value = 'test';
    document.forms[0].submit();
  };
})();

deleteFeed = (function() {
  return _AJAX?
  function(feed_id) {
    alert('Ajax function');
  }:
  function (feed_id)
  {
    document.forms[0].action.value = 'delete';
    document.forms[0].feed_id.value = feed_id;
    document.forms[0].submit();
  };
})();

saveFeed = (function() {
  return _AJAX?
  function() {
    alert('Ajax function');
  }:
  function() {
    document.forms[0].action.value = 'save';
    document.forms[0].submit();
  };
})();

clearFeed = (function() {
  return _AJAX?
  function() {
    alert('Ajax function');
  }:
  function() {
    document.location.reload();
  };
})();

editFeed = (function() {
  return _AJAX?
  function(feed_id) {
    alert('Ajax function');
  }:
  function(feed_id) {
    document.forms[0].action.value = 'edit';
    document.forms[0].feed_id.value = feed_id;
    document.forms[0].submit();
  };
})();

logout = function() {
  document.location = '/_ah/login?action=Logout&continue=/'
};

