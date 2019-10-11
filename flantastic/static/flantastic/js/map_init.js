function onEachFeature(feature, layer) {
    if (feature.properties && feature.properties.enseigne) {
        layer.bindPopup(feature.properties.enseigne);
    }
}


function set_closest_bakeries_json(dataurl, map) {
    // Download GeoJSON via Ajax
    fetch(dataurl).then(resp => {
        return resp.json();
    }).then(data => {
        L.geoJson(data, {
            onEachFeature: onEachFeature
        }).addTo(map);
    });

}


function onLocationFound(e) {
    var radius = e.accuracy / 2;
    console.log(e.latlng)
    L.marker(e.latlng).addTo(map)
    L.circle(e.latlng, radius).addTo(map);
}

//TODO: Need to change the init order:
// 1. Init map font
// 2. Get user position.
// 3. THEN get closests bakeries
// 4. Stylish the bakeries.
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

var bakeries = L.layerGroup([]);
var overlayMaps = {
    "Boulangeries": bakeries
};

L.control.layers(baseMaps, overlayMaps).addTo(map);

map.on('locationfound', onLocationFound);
map.locate({
    setView: true,
    watch: false,
    maxZoom: 16
});