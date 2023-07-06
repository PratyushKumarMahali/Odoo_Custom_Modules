/*
Quocent Pvt. Ltd.
Copyright (C) Quocent Pvt. Ltd.
All Rights Reserved
https://www.quocent.com
*/


// New Implementation
odoo.define('quocent_customer_portal_signup.login_captcha', function (require) {
    "use strict";
	
	// Importing the required module
    var core = require('web.core');
    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');

    publicWidget.registry.LoginForm = publicWidget.Widget.extend({
    	// Targeting the DOM element with the class name
        selector: '.oe_login_form',
        // Attaching method to the 'submit' event
        events: {
            'submit': '_onSubmit',
        },
        // Defining the 'start' method
        start: async function () {
        	// Calling the parent method '_super'
            this._super.apply(this, arguments);
            var self = this;
            // Making an asynchronous AJAX request to fetch the value of 'login_captcha' from the server
            var enableCaptcha = await ajax.jsonRpc('/login_captcha_value', 'http', {});
            this.enableCaptcha = enableCaptcha;
            if (this.enableCaptcha) {
            	// Loading the JavaScript file from the specified URL
                await ajax.loadJS('https://www.recaptcha.net/recaptcha/api.js');
            }
        },
        // Defining the '_onSubmit' method with an event parameter 'e'
        _onSubmit: function (e) {
            if (this.enableCaptcha && typeof grecaptcha !== 'undefined') {
                var recaptchaResponse = grecaptcha.getResponse();
                if (!recaptchaResponse) {
                    e.preventDefault();
                    $('#err').text("Please verify Captcha");
                }
            }
        },
    });
});

// Old Implementation
/*
odoo.define('quocent_customer_portal_signup.login_captcha', function (require) {
	"use strict";

	var core = require('web.core');
	var publicWidget = require('web.public.widget');
	var _t = core._t;
	const {ReCaptcha} = require('google_recaptcha.ReCaptchaV3');
	const ajax = require('web.ajax');

	publicWidget.registry.LoginForm = publicWidget.Widget.extend({
    	selector: '.oe_login_form',
    	events: {
        	'submit': '_onSubmit',
    	},
    	_onSubmit: async function (e) {
        	ajax.loadJS('https://www.recaptcha.net/recaptcha/api.js');
        	var recaptcha = $("#g-recaptcha-response").val();
        	if (recaptcha === undefined || recaptcha === null) {
            	e.preventDefault();
            	$('#err').innerHTML="Please verify Captcha";
        	} else {
        		$('.btn-primary').click();
        	}
    	},
	});

	publicWidget.registry.SignUpForm = publicWidget.Widget.extend({
	    selector: '.oe_signup_form',
	    events: {
	        'submit': '_onSubmit',
	    },
	    _onSubmit: function () {
	        e.preventDefault();
	        console.log("Signup Submits");
	        ajax.loadJS('https://www.recaptcha.net/recaptcha/api.js');
	        var $btn = this.$('.oe_login_buttons > button[type="submit"]');
	        $btn.attr('disabled', 'disabled');
	        $btn.prepend('<i class="fa fa-refresh fa-spin"/> ');
	        var recaptcha = $("#g-recaptcha-response").val();
	        if (recaptcha === undefined || recaptcha === null) {
	            e.preventDefault();
	            $('#err').innerHTML="Please verify Captcha";
	        } else {
				$('.btn-primary').click();
			}
		},
	});
	
});
*/