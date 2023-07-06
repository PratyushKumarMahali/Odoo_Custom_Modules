/*
Quocent Pvt. Ltd.
Copyright (C) Quocent Pvt. Ltd.
All Rights Reserved
https://www.quocent.com
*/

odoo.define('quocent_customer_portal_signup.signup_validation', function (require) {
	"use strict";
	
	var ajax = require('web.ajax');
	require('web.dom_ready');

	var $signupForm = $('.oe_signup_form');
	if (!$signupForm.length) {
		return;
	}
	
	// Old Implementation
	/*
	var btnPrimary = $('.btn-primary');
	btnPrimary.click(function(e){
    	console.log("Signup Submits");
    	var recaptcha = $("#g-recaptcha-response").val();
    	if (recaptcha === undefined || recaptcha === null) {
        	e.preventDefault();
        	ajax.loadJS('https://www.recaptcha.net/recaptcha/api.js');
        	$('#err').innerHTML="Please verify Captcha";
    	} else {
    		$('.btn-primary').click();
    	}
	});
	*/

	var $cust_code = $('[name=cust_code]');
	var $customer_name = $('[name=name]');
	$cust_code.on('change', function () {
    	let cust_code_val = $cust_code.val();
    	console.log("cust_code_val > ", cust_code_val);
    	if(cust_code_val && cust_code_val.length){
        	ajax.jsonRpc('/get/partner/name', 'call', {'code': cust_code_val}).then(function (result) {
            	console.log("result", result);
            	if (result == 'error') {
            		$customer_name.val('');
            	} else {
                	$customer_name.val(result.name);
                	$('[name=pan_num]').val(result.pan);
                	$('[name=gst_num]').val(result.gst);
                	$('[name=phone_num]').val(result.phone);
                	$('[name=login]').val(result.email);
            	}
        	});
  		}
  		if (($phone_num.val().length == 0) || ($gst_num.val().length == 0) || ($pan_num.val().length == 0)) {
        	$('.btn-primary').prop('disabled', true);
    	} else {
        	$('.btn-primary').prop('disabled', false);
    	}
	});

	var $pan_num = $('[name=pan_num]');
	$pan_num.on('change', function () {
    	let pan_val = $pan_num.val();
		let warning_html = `<div class="qcent_pan_alert alert alert-warning small pt-2 pb-2">PAN # is not valid.</div>`;
    	if(pan_val && pan_val.length) {
        	if(! /([A-Z]){5}([0-9]){4}([A-Z]){1}$/.test(pan_val)) {
            	if($('.qcent_pan_alert').length == 0) {
                	$(warning_html).insertAfter(".oe_signup_form [name=pan_num]");
            	}
        	} else {
            	$('.qcent_pan_alert').remove();
        	}
  		} else {
        	$('.qcent_pan_alert').remove();
    	}
	});

	var $gst_num = $('[name=gst_num]');
	$gst_num.on('change', function () {
    	let gst_val = $gst_num.val();
		let warning_html = `<div class="qcent_gst_alert alert alert-warning small pt-2 pb-2">GST # is not valid.</div>`;
    	if(gst_val && gst_val.length) {
        	if(! /^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$/.test(gst_val)) {
            	if($('.qcent_gst_alert').length == 0) {
                	$(warning_html).insertAfter(".oe_signup_form [name=gst_num]");
            	}
        	} else {
            	$('.qcent_gst_alert').remove();
        	}
  		} else {
        	$('.qcent_gst_alert').remove();
    	}
	});

	var $phone_num = $('[name=phone_num]');
	$phone_num.on('change', function () {
	    let phone_val = $phone_num.val();
		let warning_html = `<div class="qcent_phone_alert alert alert-warning small pt-2 pb-2">Phone # is not valid.</div>`;
	    if(phone_val && phone_val.length) {
	        if(! $.isNumeric(phone_val)) {
	            if($('.qcent_phone_alert').length == 0) {
	                $(warning_html).insertAfter(".oe_signup_form [name=phone_num]");
	            }
	        } else {
	            $('.qcent_phone_alert').remove();
	        }
	  	} else {
	        $('.qcent_phone_alert').remove();
	    }
	});
	
	// New Implementation
	// Importing the required module
	var core = require('web.core');
	var publicWidget = require('web.public.widget');
	
	// Override the '/addons/auth_signup/static/src/js/signup.js' file and replacing it with custom code
	publicWidget.registry.SignUpForm = publicWidget.registry.SignUpForm.extend({
		// Targeting the DOM element with the class name
		selector: '.oe_signup_form',
		// Attaching method to the 'submit' event
		events: {
            'submit': '_onSubmit',
        },
        // Defining the 'start' method
        start: async function () {
        	// Calling the parent method '_super'
            this._super.apply(this, arguments);
            var self = this;
            // Making an asynchronous AJAX request to fetch the value of 'signup_captcha' from the server
            var enableCaptcha = await ajax.jsonRpc('/signup_captcha_value', 'http', {});
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
                    e.stopImmediatePropagation();
                    $('#err').text("Please verify Captcha");
                    return false;
                } else {
                	var $btn = this.$('.oe_login_buttons > button[type="submit"]');
        			$btn.attr('disabled', 'disabled');
        			$btn.prepend('<i class="fa fa-refresh fa-spin"/> ');
        		}
            } else {
                var $btn = this.$('.oe_login_buttons > button[type="submit"]');
        		$btn.attr('disabled', 'disabled');
        		$btn.prepend('<i class="fa fa-refresh fa-spin"/> ');
        	}
        },
	});
	
});