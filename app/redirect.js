$('document').ready(function(){  	
  	// use this to avoid redirects when a user clicks "back" in their browser
	window.location.replace('http://somewhereelse.com');

	// use this to redirect, a back button call will trigger the redirection again
	window.location.href = "http://somewhereelse.com";

	// given for completeness, essentially an alias to window.location.href
	window.location = "http://somewhereelse.com";
})
