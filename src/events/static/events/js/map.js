$("#map").height(
    Math.max(Math.min($("#events").height(), 800), 500)
);

var fucked_probes = [];  // Globals are the devil

var map = L.map('map').setView([39.74739, -105], 13);
L.tileLayer('http://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
  subdomains: 'abcd',
  maxZoom: 19
}).addTo(map);


function onEachFeature(feature, layer) {

    var p = feature.properties;
    layer.bindPopup(
        '<table class="table table-responsive">' +
            '<tr><td colspan="2" class="text-center"><a href="https://atlas.ripe.net/probes/"' + p.id + '/" class="btn btn-info btn-block">#' + p.id + '</a></td></tr>' +
            '<tr><th>IPv4</th><td>' + p.address_v4 + '</td></tr>' +
            '<tr><th>IPv6</th><td>' + (p.address_v6 || "n/a") + '</td></tr>' +
        '</table>'
    );

}


function pointToLayer(feature, latlng) {
    var colour = "#999999";
    var opacity = 0.2;
    var radius = 3;
    if ($.inArray(feature.properties.id.toString(), fucked_probes) > -1) {
        colour = "#ff0000";
        opacity = 0.8;
        radius = 8;
    }

    return L.circleMarker(latlng, {
        radius: radius,
        fillColor: colour,
        color: "#666666",
        weight: 1,
        opacity: opacity,
        fillOpacity: opacity
    });
}


function getMarkers(){

    return L.geoJson(features, {
        style: function (feature) {
            return feature.properties && feature.properties.style;
        },
        onEachFeature: onEachFeature,
        pointToLayer: pointToLayer
    });

}

var markers = getMarkers();

markers.addTo(map);

self.map.fitBounds(markers.getBounds());

$(".outage").click(function(){
    fucked_probes = $(this).attr("data-probe_ids").split(",");
    map.removeLayer(markers);
    markers = getMarkers().addTo(map);
    markers.addTo(map);
});
