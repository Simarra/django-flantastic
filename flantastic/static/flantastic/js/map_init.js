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


function format_get_closests_url(base_url, id_not_to_get, longlat, bbox_ne, bbox_sw) {
    let res = base_url + "bakerie_arround/pos/" +
        id_not_to_get + "/" +
        longlat + "/" +
        bbox_ne + "/" +
        bbox_sw + "/";
    return res;

}

function _format_point_for_api(lng, lat) {
    // Format point for the backend;

    let latlong = "(" + lng + "," + lat + ")";
    return latlong

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

async function add_closest_bakeries_json(longlat, id_not_to_get, bbox_ne, bbox_sw) {
    // Download GeoJSON via Ajax

    let formated_url = format_get_closests_url(dataurl, id_not_to_get, longlat, bbox_ne, bbox_sw)

    let res = await fetch(formated_url);
    let json_res = await res.json();

    add_data_to_gjson(json_res);

}


function onLocationFound(e) {
    var radius = e.accuracy / 2;
    L.marker(e.latlng).addTo(map);
    L.circle(e.latlng, radius).addTo(map);
    let id_not_to_get = "99999999";
    let latlong = _format_point_for_api(e.longitude, e.latitude);
    let bbox = map.getBounds();
    console.log(bbox)

    let bbox_ne = _format_point_for_api(bbox._northEast.lng, bbox._northEast.lat);
    let bbox_sw = _format_point_for_api(bbox._southWest.lng, bbox._southWest.lat);
    add_closest_bakeries_json(latlong, id_not_to_get, bbox_ne, bbox_sw);
}

function add_data_to_gjson(json_to_add) {
    // FIXME: BUG: Gjson updated but not the map :'()
    for (let feat_id in json_to_add.features) {
        gjson.features.push(json_to_add.features[feat_id])
    }
    feature_group.addData(json_to_add)
}

async function set_user_bakeries() {
    if (is_authenticated == true) {
        let res = await fetch(user_bakeries_url);
        let json_res = await res.json();

        add_data_to_gjson(json_res);
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
var bakeries_lyr = L.layerGroup([]);
var overlayMaps = {
    "Boulangeries": bakeries_lyr
};

var gjson = {
    "type": "FeatureCollection",
    "crs": { "type": "name", "properties": { "name": "EPSG:4326" } },
    "features": []
}

var feature_group = L.geoJson(gjson, {
    onEachFeature: onEachFeature
})

feature_group.addTo(bakeries_lyr).on("click", signal_markup_clicked);


bakeries_lyr.addTo(map);

L.control.layers(baseMaps, overlayMaps).addTo(map);

set_user_bakeries();
// Add position and closest points
map.on('locationfound', onLocationFound);


map.on('click', signal_empty_map_clicked)
map.locate({
    setView: true,
    watch: false,
    maxZoom: 16
});