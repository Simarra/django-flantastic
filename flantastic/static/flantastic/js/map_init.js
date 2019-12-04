function geoloc_available() {
    if (!"geolocation" in navigator) {
        /* la géolocalisation est disponible */
        alert("No geolocalisation support in your brower. location will be set in Paris.")
    }
}

function getFeaturesInView() {
    // Function wich retrieve data from screen bbox
    var features = [];
    map.eachLayer(function(layer) {
        if (layer instanceof L.Marker) {
            if (map.getBounds().contains(layer.getLatLng())) {
                features.push(layer.feature);
            }
        }
    });
    return features;
}

function getPkInView() {
    // retrieve pk of elts in screen bbox
    let features = getFeaturesInView()
    let res = [];
    for (elt of features) {
        if (elt) {
            res.push(elt.properties.pk);
        }
    }

    return res

}



function onEachFeature(feature, layer) {
    if (feature.properties && feature.properties.enseigne) {
        // layer.bindPopup(feature.properties.enseigne);
        layer.bindTooltip(feature.properties.enseigne, { permanent: true, className: "my-label", offset: [-10, 0], direction: "auto" });
    }
}


function pointToLayer(feature, layer) {
    var lat = feature.geometry.coordinates[1];
    var lon = feature.geometry.coordinates[0];
    let x = feature.properties.global_note;
    switch (true) {
        case undefined:
            return L.marker([lat, lon], { icon: unnotedBakeryIcon });
        case null:
            return L.marker([lat, lon], { icon: unnotedBakeryIcon });
        case 0:
            return L.marker([lat, lon], { icon: unnotedBakeryIcon });
        case (x > 0 && x < 2):
            return L.marker([lat, lon], { icon: badBakeryIcon });
        case (x >= 2 && x < 4):
            return L.marker([lat, lon], { icon: mediumBakeryIcon });
        case (x >= 4):
            return L.marker([lat, lon], { icon: goodBakeryIcon });
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
    // console.log(e.layer._leaflet_id)
    slot_markup_clicked(e.layer)
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

    add_data_to_layer(json_res);

}


function onLocationFound(e) {
    var radius = e.accuracy / 2;
    L.marker(e.latlng).addTo(map);
    L.circle(e.latlng, radius).addTo(map);
    let id_not_to_get = "99999999";
    let latlong = _format_point_for_api(e.longitude, e.latitude);
    let bbox = map.getBounds();

    let bbox_ne = _format_point_for_api(bbox._northEast.lng, bbox._northEast.lat);
    let bbox_sw = _format_point_for_api(bbox._southWest.lng, bbox._southWest.lat);
    add_closest_bakeries_json(latlong, id_not_to_get, bbox_ne, bbox_sw);
}

function add_data_to_layer(json_to_add) {
    feature_group.addData(json_to_add)
}

async function set_user_bakeries() {
    // get and set user bakeries only if user is logged
    if (is_authenticated == true) {
        let res = await fetch(user_bakeries_url);
        let json_res = await res.json();

        add_data_to_layer(json_res);
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

var bakeries_lyr = L.layerGroup([]);
var overlayMaps = {
    "Boulangeries": bakeries_lyr
};

var gjson = {
    "type": "FeatureCollection",
    "crs": { "type": "name", "properties": { "name": "EPSG:4326" } },
    "features": []
}


var BakeryIcon = L.Icon.extend({
    options: {
        iconSize: [42, 35],
        shadowSize: [50, 64],
        // iconAnchor: [88, 35],
        shadowAnchor: [4, 62],
        popupAnchor: [40, -76]
    }
});

var unnotedBakeryIcon = new BakeryIcon({ iconUrl: unnoted_bakery_icon_path }),
    badBakeryIcon = new BakeryIcon({ iconUrl: bad_bakery_icon_path }),
    mediumBakeryIcon = new BakeryIcon({ iconUrl: medium_bakery_icon_path }),
    goodBakeryIcon = new BakeryIcon({ iconUrl: good_bakery_icon_path });

var feature_group = L.geoJson(gjson, {
    onEachFeature: onEachFeature,
    pointToLayer: pointToLayer
})

feature_group.addTo(bakeries_lyr).on("click", signal_markup_clicked);


bakeries_lyr.addTo(map);

L.control.layers(baseMaps, overlayMaps).addTo(map);

if (is_authenticated == true) {
    set_user_bakeries()
};
// Add position and closest points
map.on('locationfound', onLocationFound);


map.on('click', signal_empty_map_clicked)
map.locate({
    setView: true,
    watch: false,
    maxZoom: 16
});

map.on('moveend', function(e) {
    // Add points when moving on map. Limited to 500
    if (feature_group.getLayers().lenght > 200) {
        return;
    }
    if (map.getZoom() < 17) {
        return
    }

    let pks = getPkInView();
    if (pks.length == 0) {
        pks.push("999999")
    }

    let id_not_to_get = pks.join("-");

    let map_center = map.getCenter();
    let latlong = _format_point_for_api(map_center.lng, map_center.lat);
    let bbox = map.getBounds();

    let bbox_ne = _format_point_for_api(bbox._northEast.lng, bbox._northEast.lat);
    let bbox_sw = _format_point_for_api(bbox._southWest.lng, bbox._southWest.lat);
    add_closest_bakeries_json(latlong, id_not_to_get, bbox_ne, bbox_sw);

});