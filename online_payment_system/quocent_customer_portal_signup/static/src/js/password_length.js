/*
Quocent Pvt. Ltd.
Copyright (C) Quocent Pvt. Ltd.
All Rights Reserved
https://www.quocent.com
*/
odoo.define('quocent_customer_portal_signup.policy', function (require) {
"use strict";

require('web.dom_ready');

var $signupForm = $('.oe_signup_form, .oe_reset_password_form');
if (!$signupForm.length) { return; }
var $password = $('[type=password][minlength]');

$password.on('change', function () {
    let pass_val = $password.val();
	let is_error = false;
	let warning_html = `<div class="qcent_alert alert alert-warning small pt-2 pb-2">
                            Password having 8 characters length is expected.
                            <br/>
                            Should also followed below criteria:
                            <br/>
                            * Must have atleast 1 numeric character
                            <br/>
                            * Must have atleast 1 special character
                        </div>`;

    if(pass_val && pass_val.length){
			if(pass_val.length<8){
				is_error = true;
			}else if($.isNumeric(pass_val)){
				is_error = true;
			}else if(/^[a-zA-Z]+$/.test(pass_val)){
				is_error = true;
			}
			if(is_error){
				$(".oe_signup_form #password").val('');
				$(".oe_signup_form #password").focus();
				$(".oe_signup_form .btn-block").prop('disabled', true);
				$(warning_html).insertAfter(".oe_signup_form .field-password");
			}
  		}

});

$password.on('input', function () {
	$(".oe_signup_form .btn-block").prop('disabled', false);
    $("div.qcent_alert").remove();

});

});