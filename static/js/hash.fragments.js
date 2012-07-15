$(function(){
            
  // Bind an event to window.onhashchange that, when the history state changes,
  // gets the url from the hash and displays either our cached content or fetches
  // new content to be displayed.
  $(window).bind( 'hashchange', function(e) {
    
    // Get the hash (fragment) as a string, with any leading # removed. Note that
    // in jQuery 1.4, you should use e.fragment instead of $.param.fragment().
    var url = $.param.fragment();
    
    // Remove .bbq-current class from any previously "current" link(s).
    $( 'a.bbq-current' ).removeClass( 'bbq-current' );
    
    if(url)
    {
        $(".bbq-default").hide();
    // Add .bbq-current class to "current" nav link(s), only if url isn't empty.
    url && $( 'a[href="#!' + url + '"]' ).addClass( 'bbq-current' );

  // Show "loading" content while AJAX content loads.
  $( '.bbq-loading' ).show();
// Load external content via AJAX. Note that in order to keep this
// example streamlined, only the content in .infobox is shown. You'll
// want to change this based on your needs.
  $('.bbq-item').load( url, function(){
      // Content loaded, hide "loading" content.
      $( '.bbq-loading' ).hide();
      $( '.bbq-item' ).show();
    });
    }
    else
    {
        $(".bbq-item").hide();
        $(".bbq-default").show();
    }
  })
});

