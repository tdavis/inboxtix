qtipConfigVertical = {
    show: { 
        ready: true, 
        when: { event: 'blur' }
    },
    hide: { when: { event: 'focus' } },
    style: { 
        name: 'cream',
        tip:  {
            corner: 'topMiddle',
            size: { x:12, y:6 }
        },
        width: { min: 360, max: 360 }
    },
    position: {
        corner: {
            tooltip: 'topMiddle',
            target: 'bottomMiddle'
        },
        adjust: {
            x: 0,
            y: 2
        }
    }
}

qtipConfigHorizontal = $.extend(true, {}, qtipConfigVertical);
qtipConfigHorizontal['style']['width'] = { min: 230, max: 230 };
qtipConfigHorizontal['position']['adjust']['y'] = 0;
qtipConfigHorizontal['position']['adjust']['x'] = 2;
qtipConfigHorizontal['position']['corner'] = { 
    tooltip: 'leftMiddle',
    target: 'rightMiddle'
};
qtipConfigHorizontal['style']['tip']['size'] = { x:6, y:12 }
qtipConfigHorizontal['style']['tip']['corner'] = 'leftMiddle';
// Autocomplete
$("#id_category_id").autocomplete("/get_categories/", {
    minChars: 3,
    width: 358,
    cacheLength: 10,
});

var beforeSubmit = function(data, obj, opts) {
    $('.qtip').remove();
    container = $('#signup-form');
    obj.hide();
    container.append(
        '<p id="submitting"><img src="'+MEDIA_URL+'/img/indicator2.gif">Submitting...</p>'
    );
    container.animate({height:'50px'}, 500, function() {
    });
};

var success = function(data, obj, opts) {
    var container = $('#signup-form');
    if (data == '') {
        
    } else if(data == 'verify') { 
    
    } else {
        var errors = Array();
        var arr = data.split('\n');
        for(var x=0; x<arr.length; x++) {
            var arr2 = arr[x].split('::');
            var err = $(arr2[1]);
            errors[arr2[0]] = err;
        }
        $('#submitting').remove();
        container.animate({ height: '160px' }, 500, function() {
            $('#signup-form form').show();
            generateQtips(errors);
        });
    }
};

$('#signup-form form').ajaxForm({
    beforeSubmit: beforeSubmit,
    success: success
});

