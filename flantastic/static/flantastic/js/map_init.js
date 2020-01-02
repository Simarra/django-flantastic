function geoloc_available() {
    if (!"geolocation" in navigator) {
        /* la géolocalisation est disponible */
        alert("No geolocalisation support in your brower. location will be set in Paris.")
    }
}

function getFeaturesInView() {
    // Function wich retrieve data from screen bbox
    var features = [];
    let bounds = map.getBounds()
    bakeries_lyr.eachLayer(function(lyr) {
        if (bounds.contains(lyr.getLatLng())) {
            features.push(lyr)
        }
    })
    return features;
}

function getPkInView() {
    // retrieve pk of elts in screen bbox
    let features = getFeaturesInView()
    let res = [];
    for (elt of features) {
        if (elt) {
            res.push(elt.feature.properties.pk);
        }
    }

    return res

}



function onEachFeature(feature, layer) {
    if (feature.properties && feature.properties.enseigne) {
        // layer.bindPopup(feature.properties.enseigne);
        layer.bindTooltip(feature.properties.enseigne, { permanent: true, className: "my-label", offset: [-10, 0], direction: "left" });
    }
}


function pointToLayer(feature, layer) {
    var lat = feature.geometry.coordinates[1];
    var lon = feature.geometry.coordinates[0];
    let x = feature.properties.global_note;
    switch (true) {
        case (x == undefined):
            return L.marker([lat, lon], { icon: unnotedBakeryIcon });
        case (x == null):
            return L.marker([lat, lon], { icon: unnotedBakeryIcon });
        case (x == 0):
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

// LABELGUN FUNCTIONS
function resetLabels(markers) {
    //labelgun function

    var i = 0;
    markers.eachLayer(function(label) {
        addLabel(label, ++i);
    });
    labelEngine.update();

}

function addLabel(layer, id) {
    //labelgun function

    // This is ugly but there is no getContainer method on the tooltip :(
    var label = layer.getTooltip()._source._tooltip._container;
    if (label) {

        // We need the bounding rectangle of the label itself
        var rect = label.getBoundingClientRect();

        // We convert the container coordinates (screen space) to Lat/lng
        var bottomLeft = map.containerPointToLatLng([rect.left, rect.bottom]);
        var topRight = map.containerPointToLatLng([rect.right, rect.top]);
        var boundingBox = {
            bottomLeft: [bottomLeft.lng, bottomLeft.lat],
            topRight: [topRight.lng, topRight.lat]
        };

        // Ingest the label into labelgun itself
        labelEngine.ingestLabel(
            boundingBox,
            id,
            parseInt(Math.random() * (5 - 1) + 1), // Weight
            label,
            "Test " + id,
            false
        );

        // If the label hasn't been added to the map already
        // add it and set the added flag to true
        if (!layer.added) {
            layer.addTo(map);
            layer.added = true;
        }

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


// Labelgun!
// This is core of how Labelgun works. We must provide two functions, one
// that hides our labels, another that shows the labels. These are essentially
// callbacks that labelgun uses to actually show and hide our labels
// In this instance we set the labels opacity to 0 and 1 respectively. 
var hideLabel = function(label) { label.labelObject.style.opacity = 0; };
var showLabel = function(label) { label.labelObject.style.opacity = 1; };
labelEngine = new labelgun.default(hideLabel, showLabel);

var bakeries_lyr = L.markerClusterGroup.layerSupport([]);

bakeries_lyr.addTo(map).on("click", signal_markup_clicked);

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


// For each marker lets add a label
var i = 0; //TODO: Eliminate this uggly & useless i var
feature_group.eachLayer(function(label) {
    label.added = true;
    addLabel(label, i);
    i++;
});


feature_group.addTo(bakeries_lyr)



L.control.layers(baseMaps, overlayMaps).addTo(map);

if (is_authenticated == true) {
    set_user_bakeries()
};

/////////////////////
// EVENTS SETTINGS //
/////////////////////

// Add position and closest points
map.on('locationfound', onLocationFound);


map.on('click', signal_empty_map_clicked)
map.locate({
    setView: true,
    watch: false,
    maxZoom: 16
});

map.on('moveend', function(e) {
    // Add points when moving on map. Limited to 2000
    if (feature_group.getLayers().lenght > 2000) {
        resetLabels(feature_group);
        return;
    }
    if (map.getZoom() < zoom_level) {
        resetLabels(feature_group);
        return;
    }

    let pks = getPkInView();
    if (pks.length == 0) {
        pks.push("999999") // Ugly workarround. TODO: Fix API.
    }

    let id_not_to_get = pks.join("-");

    let map_center = map.getCenter();
    let latlong = _format_point_for_api(map_center.lng, map_center.lat);
    let bbox = map.getBounds();

    let bbox_ne = _format_point_for_api(bbox._northEast.lng, bbox._northEast.lat);
    let bbox_sw = _format_point_for_api(bbox._southWest.lng, bbox._southWest.lat);
    add_closest_bakeries_json(latlong, id_not_to_get, bbox_ne, bbox_sw);
    resetLabels(feature_group);

});

// labelgun when markercluster animations ends
bakeries_lyr.on('animationend', function() {
    resetLabels(feature_group);
})


resetLabels(feature_group);



/////////////////////
// CUSTOM CONTROLS //
/////////////////////
L.easyButton('<span class="target">&target;</span>', function() {
    alert('you just clicked the html entity \&target;');
}, 'Zoom on geoloc').addTo(mymap);

L.easyButton('<span class="target">&circlearrowright;</span>', function() {
    alert('you just clicked the html entity \&target;');
}, 'Zoom on geoloc').addTo(mymap);