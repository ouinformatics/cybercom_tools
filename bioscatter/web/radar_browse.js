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
        WIDTH:      $('#map1').width(),
        HEIGHT:     $('#map1').height(),
        BBOX:       params.loc,
        FORMAT:     'image/png'
    };
    var url = 'http://fire.rccc.ou.edu/cgi-bin/mapserv?' + serialize(defparams)
    return url
};

function updateUI(datetime) {
     $('#scene').val(datetime);
     $('#minute').val( new Date(datetime).toString('HH:mm') ); 
     $('#day').val( new Date(datetime).toString('M/d/yyyy') );
     //$('#text').text(datetime.toISOString());
     $(img).attr('src', makeUrl({datetime: datetime, loc: loc}) );
}

function updatePlot(startDate, nDays) {
    endDate = new Date(startDate)
    startDate = new Date("2011-02-01T00:00:00")
    endDate = new Date("2011-02-03T11:00:00")
    $.getJSON('http://fire.rccc.ou.edu/mongo/db_find?callback=?', { db: "bioscatter", col: "unqc_cref", date: 'timestamp,'+startDate.toISOString()+','+endDate.toISOString() },
        function(data) { 
            var plot_data = Array(); 
            $.each(data, 
                function(i, val) { 
                    plot_data.push([ new Date(val.timestamp), parseFloat(val.maxval) ] )
                    //loc = val.projwin[0]+','+val.proj_win[1]+','+val.proj_win[2]','+val.proj_win[3]; 
                }
            );  
            $.plot($('#plot1'), [ plot_data ], {xaxis: {mode: "time"}, grid: { clickable: Boolean("True")} } );
                });
};

updatePlot();

$("#plot1").bind("plotclick", function (event, pos, item) {
        //alert("You clicked at " + pos.x + ", " + pos.y);
        // axis coordinates for other axes, if present, are in pos.x2, pos.x3, ...
        // if you need global screen coordinates, they are pos.pageX, pos.pageY

        if (item) {
          //highlight(item.series, item.datapoint);
          updateUI(new Date(pos.x));        }
    });


$('#daySlider').slider( { value: maxDate,  
    max: maxDate.getTime(), 
    min: minDate.getTime(), 
    step: 86400000,
    stop: function(event, ui) {
        datetime =  new Date(ui.value + $('#minSlider').slider('value')).toISOString();
        updateUI(datetime);
    } 
}); 
    
$('#minSlider').slider( { value: 0, 
    min: 0, 
    max: 86400000, 
    step: 300000, 
    stop: function(event, ui) { 
        datetime = new Date(ui.value + $('#daySlider').slider('value')).toISOString();
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




