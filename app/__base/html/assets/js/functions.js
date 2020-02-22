/*global jQuery */
/* Contents
// ------------------------------------------------>
	1.  Background INSERT
	2.  HEADER AFFIX
	3.	AJAX MAILCHIMP
	4.  AJAX CAMPAIGN MONITOR 
	5.  OWL CAROUSEL
    6.  SCROLL TO
    7.  Navbar Toggler
	8.  WOW
	9.  Youtube Background
*/
(function($) {
    "use strict";

    /* ------------------  Background INSERT ------------------ */

    var $bgSection = $(".bg-section");

    $bgSection.each(function() {
        var bgSrc = $(this).children("img").attr("src");
        var bgUrl = 'url(' + bgSrc + ')';
        $(this).parent().css("backgroundImage", bgUrl);
        $(this).parent().addClass("bg-section");
        $(this).remove();
    });

    /* ------------------ HEADER AFFIX ------------------ */  
            // REMOVED IN BOOTSTRAP    v4  //  

/* 
    var $navAffix = $(".header-fixed .navbar-fixed-top");
    $navAffix.affix({
        offset: {
            top: 50
        }
    });
 */




    // Although the affix is removed from Bootstrap in version 4. However, you can achieve your goal through this jQuery Code:

    $(window).on('scroll', function(event) {
        var scrollValue = $(window).scrollTop();
        if (scrollValue > $('.navbar').scrollTop() ) {
            $('.navbar').addClass('affix');
        } else {
            $('.navbar').removeClass('affix');
        }
    });


    /* ------------------  AJAX MAILCHIMP ------------------ */

    /*$('.mailchimp').ajaxChimp({
        url: "https://api.hsforms.com/submissions/v3/integration/submit/3381861/90256be2-1abf-478b-894d-86de50094e53", //Replace with your own mailchimp Campaigns URL.
        callback: chimpCallback,
        method: "POST"
    });
    */

    /*
    function chimpCallback(resp) {
        if (resp.result === 'success') {
            $('.subscribe-alert').html('<h5 class="alert alert-success">' + resp.msg + '</h5>').fadeIn(1000);
            //$('.subscribe-alert').delay(6000).fadeOut();

        } else if (resp.result === 'error') {
            $('.subscribe-alert').html('<h5 class="alert alert-danger">' + resp.msg + '</h5>').fadeIn(1000);
        }
    }
    */

    /* ------------------  AJAX CAMPAIGN MONITOR  ------------------ */
    /*
    $('#campaignmonitor').submit(function(e) {
        e.preventDefault();
        $.getJSON(
            this.action + "?callback=?",
            $(this).serialize(),
            function(data) {
                if (data.Status === 400) {
                    alert("Error: " + data.Message);
                } else { // 200
                    alert("Success: " + data.Message);
                }
            });
    });
    /*
    /* ------------------ OWL CAROUSEL ------------------ */
    
    $(".owl-carousel").each(function() {
        var $Carousel = $(this);
        $Carousel.owlCarousel({
            loop: $Carousel.data('loop'),
            autoplay: $Carousel.data("autoplay"),
            margin: $Carousel.data('space'),
            nav: $Carousel.data('nav'),
            dots: $Carousel.data('dots'),
            dotsSpeed: $Carousel.data('speed'),
            responsive: {
                0: {
                    items: 1
                },
                600: {
                    items: $Carousel.data('slide-res')
                },
                1000: {
                    items: $Carousel.data('slide'),
                }
            }
        });
    });

    /* ------------------  SCROLL TO ------------------ */

    var aScroll = $('.nav-item .nav-link');
    aScroll.on('click', function(event) {
        var target = $($(this).attr('href'));
        $(this).parent(".nav-item").siblings().removeClass('active');
        $(this).parent('.nav-item').addClass('active');
        if (target.length > 0) {
            event.preventDefault();
            $('html, body').animate({
                scrollTop: target.offset().top - 100
            }, 1000);
        }
    });

    /* ------------------  Navbar Toggler ------------------ */
    $('.navbar-toggler').click(function() {
        $('.navbar-toggler-icon').toggleClass('active');
    });


    /* ------------------  WOW Animated ------------------ */
    var wow = new WOW({
        boxClass: 'wow', // animated element css class (default is wow)
        animateClass: 'animated', // animation css class (default is animated)
        offset: 50, // distance to the element when triggering the animation (default is 0)
        mobile: false, // trigger animations on mobile devices (default is true)
        live: true // act on asynchronously loaded content (default is true)

    });
    wow.init();

    /* ------------------  Youtube Background  ------------------ */
    $(".bg-ytvideo").each(function() {

        var vidId = $(this).data("vid-id"),
            vidAutoPlay = $(this).data("autoplay"),
            vidStartAt = $(this).data("start-at"),
            vidMute = $(this).data("mute"),
            vidOpacity = $(this).data("opacity"),
            vidShowPluginLogo = $(this).data("plugin-logo"),
            vidShowControls = $(this).data("controls"),
            vidFallBackImg = $(this).data("fall-cover");

        if (vidAutoPlay === "" || vidAutoPlay === null || vidAutoPlay === undefined) {
            vidAutoPlay = true;
        }
        if (vidStartAt === "" || vidStartAt === null || vidStartAt === undefined) {
            vidStartAt = 0;
        }
        if (vidMute === "" || vidMute === null || vidMute === undefined) {
            vidMute = true;
        }
        if (vidOpacity === "" || vidOpacity === null || vidOpacity === undefined) {
            vidOpacity = 1;
        }
        if (vidShowPluginLogo === "" || vidShowPluginLogo === null || vidShowPluginLogo === undefined) {
            vidShowPluginLogo = false;
        }
        if (vidShowControls === "" || vidShowControls === null || vidShowControls === undefined) {
            vidShowControls = false;
        }
        if (vidFallBackImg === "" || vidFallBackImg === null || vidFallBackImg === undefined) {
            vidFallBackImg = "";
        }

        $(this).data(
            "property",
            "{videoURL:'http://youtu.be/" + vidId + "',containment:'self',autoPlay:" + vidAutoPlay + ", mute:" + vidMute + ", startAt:" + vidStartAt + ", opacity:" + vidOpacity + ",showYTLogo:" + vidShowPluginLogo + ",showControls:" + vidShowControls + ",stopMovieOnBlur:false,mobileFallbackImage:'" + vidFallBackImg + "'}"
        );
    });

    $(".bg-ytvideo").mb_YTPlayer();


}(jQuery));