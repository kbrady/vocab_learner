// *************************************************************
//
// jQuery TableScroll plugin.
// ver 1.0.1
// (c) 2013 Deserted Road Studios, Corp.  All Rights Reserved.
// www.desertedroad.com
// Use freely, but do not remove this copyright notice.
//
// *************************************************************

(function ($) {
    $.fn.tableScroll = function (options) {

        var settings = $.extend({
            scrollbarWidth: 0,
            scrollHeight: 800
        }, options);

        // set class to element
        this.addClass('drsTableScroll');

        // get each table section
        var thead = $(this.children('thead')[0]);
        var tbody = $(this.children('tbody')[0]);
        var tfoot = $(this.children('tfoot')[0]);

        // insert additional <th /> for scroll bar width
        $(thead).find('tr').append('<th style="padding:0px;" />');

        // get the cells from each table section
        var headerCells = $(thead).find('th');
        var bodyCells = $(tbody).find('td');
        var footerCells = $(tfoot).find('td');

        // insert additional DOM elements to allow the separation of the scroll
        $(tbody).wrapInner('<table style="margin:0px;" />').wrapInner('<div style="height:' + settings.scrollHeight + 'px;overflow:auto;overflow-x:hidden;display:block;" />').wrapInner('<td colspan="' + headerCells.length + '" />').wrapInner('<tr />');

        // set the width for the header/first body row/footer cells
        for (var i = 0; i < headerCells.length; i++) {
            // get the greater width of the column between the header/body/footer cells
            var newWidth = $(headerCells[i]).width() > $(bodyCells[i]).width() ? $(headerCells[i]).width() : $(bodyCells[i]).width();

            if ((tfoot != undefined) && ($(footerCells[i]).width() > newWidth))
                newWidth = $(footerCells[i]).width();

            // set the width for each section, for each column
            if (i == headerCells.length - 1) // the scrollbar column
                if (navigator.appName.indexOf("Internet Explorer") > -1)
                    $(headerCells[i]).width(settings.scrollbarWidth + 16);
                else
                    $(headerCells[i]).width(settings.scrollbarWidth);
            else 
                $(headerCells[i]).width(newWidth);

            if (i < headerCells.length - 1) // set the width for the body and footer cells
            {
                //console.log(parseInt($(bodyCells[i]).css('padding-left')) + ", " + parseInt($(bodyCells[i]).css('padding-right')));
                if (navigator.appName.indexOf("Internet Explorer") > -1)
                    $(bodyCells[i]).width(newWidth + 2);
                else
                    $(bodyCells[i]).width(newWidth);

                if (tfoot != undefined)
                    $(footerCells[i]).width(newWidth);
            }
        }

        // collapse all borders
        $('head').append("<style type=\"text/css\"> .drsTableScroll * { border-collapse: collapse; } </style>");
    };
})(jQuery);
