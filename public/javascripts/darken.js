// jquery.darken v0.1
// Copyright (c) 2011 Sitekickr.com
// Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php

jQuery.fn.darken = function(options) {

	var settings = {
		'percent'	: 15
	};
	
	if ( options ) { 
		$.extend( settings, options );
	}

	$(this).each(function() {
		var darkenPercent = settings.percent;
		var rgb = $(this).css('background-color').replace('rgb(', '').replace(')', '').split(',');
		var red = $.trim(rgb[0]);
		var green = $.trim(rgb[1]);
		var blue = $.trim(rgb[2]);
				
		red = parseInt(red * (100 - darkenPercent) / 100);
		green = parseInt(green * (100 - darkenPercent) / 100);
		blue = parseInt(blue * (100 - darkenPercent) / 100);
		
		rgb = 'rgb(' + red + ', ' + green + ', ' + blue + ')';
		$(this).css('background-color', rgb);
	});
	return this;
}

jQuery.fn.lighten = function(options) {

	var settings = {
		'percent'	: 15
	};
	
	if ( options ) { 
		$.extend( settings, options );
	}

	$(this).each(function() {
		var darkenPercent = settings.percent;
		var rgb = $(this).css('background-color').replace('rgb(', '').replace(')', '').split(',');
		var red = $.trim(rgb[0]);
		var green = $.trim(rgb[1]);
		var blue = $.trim(rgb[2]);
				
		red = parseInt(red * (100 + darkenPercent) / 100);
		green = parseInt(green * (100 + darkenPercent) / 100);
		blue = parseInt(blue * (100 + darkenPercent) / 100);
		
		rgb = 'rgb(' + red + ', ' + green + ', ' + blue + ')';
		$(this).css('background-color', rgb);
	});
	return this;
}