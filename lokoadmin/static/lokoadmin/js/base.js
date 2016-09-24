function myFunction(id) {
    var x = document.getElementById(id);
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
        x.previousElementSibling.className += " w3-theme-d1";
    } else {
        x.className = x.className.replace("w3-show", "");
        x.previousElementSibling.className =
            x.previousElementSibling.className.replace(" w3-theme-d1", "");
    }
}

function openNav() {
    var x = document.getElementById("navDemo");
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else {
        x.className = x.className.replace(" w3-show", "");
    }
}

jQuery(document).ready(function ($) {
    $('.subnavbar').find('li').each(function (i) {
        var mod = i % 3;
        if (mod === 2) {
            $(this).addClass('subnavbar-open-right');
        }
    });


    $('article').each(function () {
        $(this).find('p:not(:first)').hide()
    });

    $('.more').on('click', function () {
        $(this).hide().closest('article').find('p').show();
    });

});
