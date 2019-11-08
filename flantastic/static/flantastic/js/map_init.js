
function geoloc_available() {
    if (!"geolocation" in navigator) {
        /* la géolocalisation est disponible */
        alert("No geolocalisation support in your brower. location will be set in Paris.")
    }
}


function onEachFeature(feature, layer) {
    if (feature.properties && feature.properties.enseigne) {
        // layer.bindPopup(feature.properties.enseigne);
        layer.bindTooltip(feature.properties.enseigne, { permanent: true, className: "my-label", offset: [0, 0] });
    }
}


function format_data_url(base_url, longitude, latitude) {
    let res = base_url + "/" + longitude + "/" + latitude + "/";
    return res;

}


function signal_markup_clicked(e) {
    // Change style of clicked markup
    // Open nav
    // call slot for form update
    slot_markup_clicked(e.layer.feature.properties)
}

function signal_empty_map_clicked(e) {
    // Close the side menu if it is existing
    slot_empty_map_clicked()
}

async function add_closest_bakeries_json(longitude, latitude) {
    // Download GeoJSON via Ajax
    // TODO: Add the bouding box filter.

    let formated_url = format_data_url(dataurl, longitude, latitude)

    let res = await fetch(formated_url);
    let json_res = await res.json();

    add_data_to_gjson(json_res);

}


function onLocationFound(e) {
    var radius = e.accuracy / 2;
    L.marker(e.latlng).addTo(map)
    L.circle(e.latlng, radius).addTo(map);
    add_closest_bakeries_json(e.longitude, e.latitude)
}

function add_data_to_gjson(json_to_add){
    for (let feat_id in gjson.features){
        gjson.features[feat_id] = json_to_add[feat_id]
    }
}







let watercolor = L.tileLayer("https://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.{ext}", { id: 'watercolor', attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors', 'subdomains': 'abcd', 'ext': 'jpg' })

let osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { id: 'osm', attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' });

var map = L.map('mapid', {
    zoom: 10,
    zoomControl: false,
    layers: [watercolor]
});

var baseMaps = {
    "watercolor": watercolor,
    "osm": osm
};

// Geojson containg bakeries data linked to the markers.
// TODO: Define the structure of the gjson here.
// TODO: So the methods will just add elts to existing structure
var gjson = {};

L.geoJson(gjson, {
    onEachFeature: onEachFeature
}).addTo(bakeries_lyr).on("click", signal_markup_clicked);

var bakeries_lyr = L.layerGroup([]);
var overlayMaps = {
    "Boulangeries": bakeries_lyr
};

bakeries_lyr.addTo(map);

L.control.layers(baseMaps, overlayMaps).addTo(map);

map.on('locationfound', onLocationFound);

map.on('click', signal_empty_map_clicked)
map.locate({
    setView: true,
    watch: false,
    maxZoom: 16
});