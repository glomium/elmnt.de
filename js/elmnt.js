/* affix the navbar after scroll below header */

function calc_affix_position() {
    return $('header img').outerHeight() + $('header img').offset().top + 5px;
}

$('#nav').affix({
    offset: {
        top: calc_affix_position()
    }
});

$(window).on('resize', function() {
    $('#nav').data('bs.affix').options.offset.top = calc_affix_position();
});
