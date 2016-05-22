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

var markers = L.geoJson(features, {

    style: function (feature) {
        return feature.properties && feature.properties.style;
    },

    onEachFeature: onEachFeature,

    pointToLayer: function (feature, latlng) {
        return L.circleMarker(latlng, {
            radius: 8,
            fillColor: "#ff7800",
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
        });
    }

}).addTo(map);

self.map.fitBounds(markers.getBounds());
