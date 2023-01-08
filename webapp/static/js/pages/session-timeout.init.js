/*
Template Name: Skote - Admin & Dashboard Template
Author: Themesbrand
Website: https://themesbrand.com/
Contact: themesbrand@gmail.com
File: Session Timeout Js File
*/

$.sessionTimeout({
	keepAliveUrl: "../utility/starterpage",
	logoutButton: "Logout",
	logoutUrl: "../../authentication/pages-logout",
	redirUrl: "../authentication/pages-lockscreen",
	warnAfter: 3000,
	redirAfter: 30000,
	countdownMessage: "Redirecting in {timer} seconds.",
});

$('#session-timeout-dialog  [data-dismiss=modal]').attr("data-bs-dismiss", "modal");