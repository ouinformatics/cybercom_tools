$(document).ready(function() {


var minDate = new Date(2008, 11-1, 1);
var minDate_utc = new Date( minDate.getTime() + minDate.getUTCOffset() * 36000000 );
var maxDate = new Date(2011, 3-1, 14);
    
//$('#date').datepicker({ minDate: new Date(2009, 11 - 1, 1), maxDate: '+1D'} );

$('#daySlider').slider( { value: maxDate,  
    max: maxDate.getTime(), 
    min: minDate.getTime(), 
    step: 86400000,
    slide: function(event, ui) {
        var day = new Date( ui.value ).toString('M/d/yyyy'); 
        $('#day').val( day );
        datetime =  new Date(ui.value + $('#minSlider').slider('value')).toISOString() 
        $('#scene').val( datetime);
        $(img).attr('src','/cgi-bin/mapserv?MAP=/scratch/www/map/radar_wms.map&SERVICE=WMS&version=1.3.0&REQUEST=GetMap&layers=nexrad-unqc_cref&CRS=epsg:4326&time='+datetime+'&WIDTH=500&HEIGHT=500&BBOX=35.75,-88.25,37.75,-86.25&FORMAT=image/png');
    } 
}); 

$('#minSlider').slider( { value: 0, 
    min: 0, 
    max: 86400000, 
    step: 300000, 
    slide: function(event, ui) { 
        var minute = new Date( ui.value ).toString('HH:mm');
        $('#minute').val( minute ); 
        datetime = new Date(ui.value + $('#daySlider').slider('value')).toISOString() 
        $('#scene').val( datetime );
        //$(img).attr('src', '/cgi-bin/mapserv?MAP=/scratch/www/map/radar_wms.map&SERVICE=WMS&version=1.3.0&REQUEST=GetMap&layers=nexrad-unqc_cref&CRS=epsg:4326&time='+datetime+'&WIDTH=2000&HEIGHT=1000&BBOX=17,-131,57,-58&FORMAT=image/png')
        $(img).attr('src', '/cgi-bin/mapserv?MAP=/scratch/www/map/radar_wms.map&SERVICE=WMS&version=1.3.0&REQUEST=GetMap&layers=nexrad-unqc_cref&CRS=epsg:4326&time='+datetime+'&WIDTH=500&HEIGHT=500&BBOX=35.75,-88.25,37.75,-86.25&FORMAT=image/png');
        //loadImage(datetime);

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
    .attr('src', '/cgi-bin/mapserv?MAP=/scratch/www/map/radar_wms.map&SERVICE=WMS&version=1.3.0&REQUEST=GetMap&layers=nexrad-unqc_cref&CRS=epsg:4328&time=2011-03-11T13:00:00Z&WIDTH=500&HEIGHT=500&BBOX=17,-131,57,-58&FORMAT=image/png');


});




