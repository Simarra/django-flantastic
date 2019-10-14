function geoloc_available() {
    if (!"geolocation" in navigator) {
        /* la géolocalisation est disponible */
        alert("No geolocalisation support in your brower. location will be set in Paris.")
    }
}


function onEachFeature(feature, layer) {
    if (feature.properties && feature.properties.enseigne) {
        layer.bindPopup(feature.properties.enseigne);
    }
}


function format_data_url(base_url, longitude, latitude) {
    let res = base_url + "/" + longitude + "/" + latitude + "/";
    return res;

}

function set_closest_bakeries_json(longitude, latitude) {
    // Download GeoJSON via Ajax

    let formated_url = format_data_url(dataurl, longitude, latitude)

    fetch(formated_url).then(resp => {
        return resp.json();
    }).then(data => {
        L.geoJson(data, {
            onEachFeature: onEachFeature
        }).addTo(bakeries_lyr);
    });

}


function onLocationFound(e) {
    var radius = e.accuracy / 2;
    console.log(e.latlng)
    L.marker(e.latlng).addTo(map)
    L.circle(e.latlng, radius).addTo(map);
    set_closest_bakeries_json(e.longitude, e.latitude)
}








let watercolor = L.tileLayer("https://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.{ext}", { id: 'watercolor', attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors', 'subdomains': 'abcd', 'ext': 'jpg' })

let osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { id: 'osm', attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' });

var map = L.map('mapid', {
    zoom: 10,
    layers: [watercolor]
});

var baseMaps = {
    "watercolor": watercolor,
    "osm": osm
};

var bakeries_lyr = L.layerGroup([]);
var overlayMaps = {
    "Boulangeries": bakeries_lyr
};

L.control.layers(baseMaps, overlayMaps).addTo(map);

map.on('locationfound', onLocationFound);
map.locate({
    setView: true,
    watch: false,
    maxZoom: 16
});

console.log(window.bakeries_lyr)