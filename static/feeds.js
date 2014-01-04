function testFeed()
{
  document.forms[0].action.value = "test";
  document.forms[0].submit();
}

function deleteFeed(feed_id)
{
  document.forms[0].action.value = "delete";
  document.forms[0].feed_id.value = feed_id;
  document.forms[0].submit();
}

function saveFeed()
{
  document.forms[0].action.value = "save";
  document.forms[0].submit();
}

function clearFeed()
{
  document.location.reload();
}

function editFeed(feed_id)
{
  document.forms[0].action.value = "edit";
  document.forms[0].feed_id.value = feed_id;
  document.forms[0].submit();
}



