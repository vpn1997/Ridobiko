 $(document).ready(function()
           {
           $('#login').hover(function()
           {
               $(this).find('.drop').stop().slideToggle(100);
                
               
           });
           });


jQuery(document).ready(function()
                              {
             var navOffset = jQuery('.header_wrapper').offset().top;
            jQuery(window).scroll(function()
                                 {
              var scrollpos = jQuery(window).scrollTop();
       /*       jQuery(".header-top").html(scrollpos);  */
                if(scrollpos >=32){
                    
                    jQuery('.header_wrapper').addClass("fixed");
                    
                }else{
                            jQuery('.header_wrapper').removeClass("fixed");
                }
            });
        });