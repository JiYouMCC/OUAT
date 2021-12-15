// chat windows height setting
$(window).resize(function() {
    $("#left_pannel").height(window.innerHeight - 94);
    $("#messages").height(window.innerHeight - 265);
    $("#history_message").height(window.innerHeight - 265);
    $("#history_menu").height(window.innerHeight - 265);
});
$(window).load(function() {
    $(window).resize();
});