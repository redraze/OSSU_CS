// Google Map
var map;

// markers for map
var markers = [];

// info window
var info = new google.maps.InfoWindow;

// execute when the DOM is fully loaded
$(document).ready(function() {

    // styles for map
    // https://developers.google.com/maps/documentation/javascript/styling
    var styles = [

        // hide Google's labels
        {
            featureType: "all",
            elementType: "labels",
            stylers: [
                {visibility: "on"}
            ]
        },

        // hide roads
        {
            featureType: "road",
            elementType: "geometry",
            stylers: [
                {visibility: "off"}
            ]
        }

    ];

    // options for map
    // https://developers.google.com/maps/documentation/javascript/reference#MapOptions
    var options = {
        center: {lat: 47.6062, lng: -122.3321}, // Seattle, Washington.
        // center: {lat: 31.2304, lng: 121.4737}, // Shanghai, China.
        disableDefaultUI: true,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        maxZoom: 14,
        panControl: true,
        styles: styles,
        zoom: 8,
        zoomControl: true
    };

    // get DOM node in which map will be instantiated
    var canvas = $("#map-canvas").get(0);

    // instantiate map
    map = new google.maps.Map(canvas, options);

    // configure UI once Google Map is idle (i.e., loaded)
    google.maps.event.addListenerOnce(map, "idle", configure);

});

/**
 * Configures application (after map is in idle state).
 */
function configure()
{
    // update UI after map has been dragged
    google.maps.event.addListener(map, "dragend", function() {

        // if info window isn't open
        // http://stackoverflow.com/a/12410385
        if (!info.getMap || !info.getMap())
        {
            update();
        }
    });

    // update UI after zoom level changes
    google.maps.event.addListener(map, "zoom_changed", function() {
        update();
    });

    // configure typeahead
    $("#q").typeahead({
        highlight: false,
        minLength: 1
    },
    {
        display: function(suggestion) { return null; },
        limit: 10,
        source: search,
        templates: {
            notFound: [
                "<div class='TA_notFound'>" +
                "No results found..." +
                "</div>"
            ].join('\n'),
            pending: [
                "<div class='TA_pending'>" +
                "Searching..." +
                "</div>"
            ],
            suggestion: Handlebars.compile(
                "<div 'TA_suggestion>" +
                "{{place_name}}, {{admin_name1}}, {{postal_code}}" +
                "</div>"
            )
        }
    });

    // re-center map and add marker after place is selected from drop-down
    $("#q").on("typeahead:selected", function(eventObject, suggestion, name) {

        // set map's center
        map.setCenter({lat: parseFloat(suggestion.latitude), lng: parseFloat(suggestion.longitude)});

        // add marker from selection
        addMarker(suggestion);
    });

    // hide info window when text box has focus
    $("#q").focus(function(eventData) {
        info.close();
    });

    // re-enable ctrl- and right-clicking (and thus Inspect Element) on Google Map
    // https://chrome.google.com/webstore/detail/allow-right-click/hompjdfbfmmmgflfjdlnkohcplmboaeo?hl=en
    document.addEventListener("contextmenu", function(event) {
        event.returnValue = true;
        event.stopPropagation && event.stopPropagation();
        event.cancelBubble && event.cancelBubble();
    }, true);

    // update UI
    update();

    // give focus to text box
    $("#q").focus();
}

/**
 * Searches database for typeahead's suggestions.
 */
function search(query, syncResults, asyncResults)
{
    var parameters = {
        q : query
    };
    // get places matching query (asynchronously)
    $.getJSON(Flask.url_for("search"), parameters)
    .done(function(data, textStatus, jqXHR) {

        // call typeahead's callback with search results
        asyncResults(data);
    })
    .fail(function(jqXHR, textStatus, errorThrown) {

        // log error to browser's console
        console.log(errorThrown.toString());

        // call typeahead's callback with no results
        asyncResults([]);
    });
}

/**
 * Updates UI's markers.
 */
function update()
{
    // get map's bounds
    var bounds = map.getBounds();
    var ne = bounds.getNorthEast();
    var sw = bounds.getSouthWest();

    // get places within bounds (asynchronously)
    var parameters = {
        ne: ne.lat() + "," + ne.lng(),
        q: $("#q").val(),
        sw: sw.lat() + "," + sw.lng()
    };
    $.getJSON(Flask.url_for("update"), parameters)
    .done(function(data, textStatus, jqXHR) {

       // remove old markers from map
       removeMarkers();

       // add new markers to map
       for (var i = 0; i < data.length; i++)
       {
           addMarker(data[i]);
       }
    })
    .fail(function(jqXHR, textStatus, errorThrown) {

        // log error to browser's console
        console.log(errorThrown.toString());
    });
};

/**
 * Adds marker for place to map.
 */
function addMarker(place)
{
    var latlng = new google.maps.LatLng(place.latitude, place.longitude);
    var marker = new google.maps.Marker({
        position: latlng
    });
    markers.push(marker);
    marker.setMap(map);

    marker.addListener('click', function(){
        var parameters = {
            geo: place.postal_code
        };
        jax = $.getJSON(Flask.url_for("articles"), parameters)
        .done(function(data, textStatus, jqXHR) {
            console.log(data);
            showInfo(marker, data);
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
            console.log(errorThrown.toString());
        });
    });
}

/**
 * Shows info window at marker with content.
 */
function showInfo(marker, content)
{
    // start div
    var div = "<div id='info'>";
    if (typeof(content) == "undefined")
    {
        // http://www.ajaxload.info/
        div += "<img alt='loading' src='/static/ajax-loader.gif'/>";
    }
    else
    {
        for (var i = 0; i < 5; i++) {
            div += "<a href='" + content[i]["link"] + "' target='_blank'>" + content[i]["title"] + "</a></br>";
        }
    }

    // end div
    div += "</div>";

    // set info window's content
    info.setContent(div);

    // open info window (if not already open)
    info.open(map, marker);
}

/**
 * Removes markers from map.
 */
function removeMarkers()
{
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers = [];
}
