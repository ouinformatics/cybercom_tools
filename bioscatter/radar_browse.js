$(document).ready(function() {

var minDate = new Date('November 1, 2008 00:00:00 GMT');
var maxDate = new Date('March 31, 2011 00:00:00 GMT');

var loc = '35.75,-88.25,37.75,-86.25'

serialize = function(obj) {
  var str = [];
  for(var p in obj)
     str.push(p + "=" + encodeURIComponent(obj[p]));
  return str.join("&");
};

$('#scene').val(maxDate.toISOString())


function makeUrl(params) {
    defparams = { 
        MAP:        '/scratch/www/map/radar_wms.map',   
        SERVICE:    'WMS',
        version:    '1.3.0',
        REQUEST:    'GetMap',
        layers:     'nexrad-unqc_cref',
        CRS:        'epsg:4326',
        time:       params.datetime,
        WIDTH:      500,
        HEIGHT:     500,
        BBOX:       params.loc,
        FORMAT:     'image/png'
    };
    var url = '/cgi-bin/mapserv?' + serialize(defparams)
    return url
};

function updateUI(datetime) {
     $('#scene').val(datetime);
     $('#minute').val( new Date(datetime).setTimezone('GMT').toString('HH:mm') ); 
     $('#day').val( new Date(datetime).setTimezone('GMT').toString('M/d/yyyy') );
}

$('#daySlider').slider( { value: maxDate,  
    max: maxDate.getTime(), 
    min: minDate.getTime(), 
    step: 86400000,
    slide: function(event, ui) {
        datetime =  new Date(ui.value + $('#minSlider').slider('value')).toISOString();
        $(img).attr('src',makeUrl({datetime: datetime, loc: loc}) );
        updateUI(datetime);
    } 
}); 

$('#minSlider').slider( { value: 0, 
    min: 0, 
    max: 86400000, 
    step: 300000, 
    slide: function(event, ui) { 
        datetime = new Date(ui.value + $('#daySlider').slider('value')).toISOString();
        $(img).attr('src', makeUrl({datetime: datetime, loc: loc}) );
        updateUI(datetime);
    }
}); 

  var img = new Image();
  
  // wrap our new image in jQuery, then:
  $(img)
    // once the image has loaded, execute this code
    .load(function () {
      // set the image hidden by default    
      $(this).hide();
    
      // with the holding div #loader, apply:
      $('#loader')
        // remove the loading class (so no background spinner), 
        .removeClass('loading')
        // then insert our image
        .append(this);
    
      // fade our image in to create a nice effect
      $(this).fadeIn();
    })
    
    // if there was an error loading the image, react accordingly
    .error(function () {
      // notify the user that the image could not be loaded
    })
    
    // *finally*, set the src attribute of the new image to our image
    .attr('src', getUrl(datetime, loc));


});




