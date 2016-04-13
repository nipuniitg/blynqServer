$(document).ready(
          function(){
              var sideBarHeight = $(window).height();
              var headerHeight = $('header.header').height();
              var aHeight = sideBarHeight - headerHeight -10;
              $('.wrapper-fluid').css({height: aHeight+"px"})
          }
      );
