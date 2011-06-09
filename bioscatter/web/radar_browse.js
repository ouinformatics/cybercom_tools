$(document).ready(function() {

var minDate = new Date('2008-11-01T00:00:00Z');
var maxDate = new Date('2011-05-01T00:00:00Z');

//var startDate = new Date().today('-1d')

var loc = '35.75,-88.25,37.75,-86.25'
var loc = '34.2,-98.4,36.2,-96.4'


// Nice URL building from JSON arrays
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
        WIDTH:      $('#map1').width(),
        HEIGHT:     $('#map1').height(),
        BBOX:       params.loc,
        FORMAT:     'image/png'
    };
    var url = 'http://fire.rccc.ou.edu/cgi-bin/mapserv?' + serialize(defparams)
    return url
};

function updateUI(datetime) {
     dt = new Date(Date.parse(datetime))
     
     $('#datestring').text(dt.toJSON());
     $('#daySlider').slider({value: dt});
     utc_day = new Date(dt.getUTCFullYear(), dt.getUTCDay(), dt.getUTCMonth(), 0, 0, 0, 0);
     utc_dt = new Date(dt.getUTCFullYear(), dt.getUTCDay(), dt.getUTCMonth(), dt.getUTCHours(), dt.getUTCMinutes(), 0, 0)
     t = utc_dt.getTime() - utc_day.getTime(); 
     $('#text').text(t) 
    $('#minSlider').slider({value: t});
     $(img).attr('src', makeUrl({datetime: dt.toJSON(), loc: loc}) );
}

function updatePlot(startDate, nDays) {
    endDate = new Date(startDate)
    startDate = new Date("2011-02-01T00:00:00")
    endDate = new Date("2011-02-01T22:00:00")
    $.getJSON('http://fire.rccc.ou.edu/mongo/db_find?callback=?', { db: "bioscatter", col: "unqc_cref", date: 'timestamp,'+startDate.toISOString()+','+endDate.toISOString() },
        function(data) { 
            var plot_data = Array(); 
            $.each(data, 
                function(i, val) { 
                    plot_data.push([ new Date(val.timestamp), parseFloat(val.maxval) ] )
                    //loc = val.projwin[0]+','+val.proj_win[1]+','+val.proj_win[2]','+val.proj_win[3]; 
                }
            );  
            $.plot($('#plot1'), [ plot_data ], {xaxis: {mode: "time"}, grid: { clickable: Boolean("True")}, points: {show:true}, lines: {show:true} } );
                });
}

updatePlot();

$("#plot1").bind("plotclick", function (event, pos, item) {
        //alert("You clicked at " + pos.x + ", " + pos.y);
        // axis coordinates for other axes, if present, are in pos.x2, pos.x3, ...
        // if you need global screen coordinates, they are pos.pageX, pos.pageY

        if (item) {
          //highlight(item.series, item.datapoint);
          updateUI(new Date(item.datapoint[0]).toJSON() );
          //$('#text').text(JSON.stringify(item.datapoint)); 
      }
    });


$('#daySlider').slider( { value: maxDate,  
    max: maxDate.getTime(), 
    min: minDate.getTime(), 
    step: 86400000,
    stop: function(event, ui) {
        datetime =  new Date(ui.value + $('#minSlider').slider('value')).toJSON();
        updateUI(datetime);
    } 
}); 
    
$('#minSlider').slider( { value: 0, 
    min: 0, 
    max: 86400000, 
    step: 300000, 
    stop: function(event, ui) { 
        datetime = new Date(ui.value + $('#daySlider').slider('value')).toJSON();
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
      $('#map1')
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




