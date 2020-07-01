
  var txt;
  if (confirm("Help us serve you better, Press Ok to allow location access!")) 
  {
    txt = "Access Given!";

  } 
  else 
  {
    txt = "Access Denied!";
  }
  document.getElementById("demo").innerHTML = txt;
