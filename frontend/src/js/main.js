
(function($) {

	var	$window = $(window),
		$body = $('body');

	// // Breakpoints.
	// 	breakpoints({
	// 		xlarge:  [ '1281px',  '1680px' ],
	// 		large:   [ '981px',   '1280px' ],
	// 		medium:  [ '737px',   '980px'  ],
	// 		small:   [ null,      '736px'  ]
	// 	});

	// Play initial animations on page load.
		$window.on('load', function() {
			window.setTimeout(function() {
				$body.removeClass('is-preload');
			}, 100);
		});

	// Dropdowns.
        $('#nav > ul').dropotron({
            mode: 'fade',
            noOpenerFade: true,
            speed: 300
        });
        // $('#nav > ul').dropotron();
		// $('#nav > ul').dropotron({
        //         selectorParent:		$('#nav'),		// Parent jQuery object
        //         baseZIndex:			1000,		// Base Z-Index
        //         menuClass:			'dropotron',// Menu class (assigned to every <ul>)
        //         expandMode:			'hover',	// Expansion mode ("hover" or "click")
        //         hoverDelay:			150,		// Hover delay (in ms)
        //         hideDelay:			250,		// Hide delay (in ms; 0 disables)
        //         openerClass:		'opener',	// Opener class
        //         openerActiveClass:	'active',	// Active opener class
        //         submenuClassPrefix:	'level-',	// Submenu class prefix
        //         mode:				'fade',		// Menu mode ("instant", "fade", "slide", "zoom")
        //         speed:				'fast',		// Menu speed ("fast", "slow", or ms)
        //         easing:				'swing',	// Easing mode ("swing", "linear")
        //         alignment:			'left',		// Alignment ("left", "center", "right")
        //         offsetX:			0,			// Submenu offset X
        //         offsetY:			0,			// Submenu offset Y
        //         globalOffsetY:		0,			// Global offset Y
        //         IEOffsetX:			0,			// IE Offset X
        //         IEOffsetY:			0,			// IE Offset Y
        //         noOpenerFade:		true,		// If true and mode = "fade", prevents top-level opener fade.
        //         detach:				true,		// Detach second level menus (prevents parent style bleed).
        //         cloneOnDetach:		true		// If true and detach = true, leave original menu intact.
        // });

	// Nav.

		// Toggle.
			$(
				'<div id="navToggle">' +
					'<a href="#navPanel" class="toggle"></a>' +
				'</div>'
			)
				.appendTo($body);

		// Panel.
			$(
				'<div id="navPanel">' +
					'<nav>' +
						$('#nav').navList() +
					'</nav>' +
				'</div>'
			)
				.appendTo($body)
				.panel({
					delay: 500,
					hideOnClick: true,
					hideOnSwipe: true,
					resetScroll: true,
					resetForms: true,
					side: 'left',
					target: $body,
					visibleClass: 'navPanel-visible'
				});

})(jQuery);