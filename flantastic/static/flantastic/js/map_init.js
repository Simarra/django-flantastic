function onEachFeature(feature, layer) {
    if (feature.properties && feature.properties.enseigne) {
        layer.bindPopup(feature.properties.enseigne);
    }
}


function insert_closest_bakeries_json(dataurl, map) {
    // Download GeoJSON via Ajax
    fetch(dataurl).then(resp => {
        return resp.json();
    }).then(data => {
        L.geoJson(data, {
            onEachFeature: onEachFeature
        }).addTo(map);
    });

}



function map_init(map, options) {
    //TODO: Need to change the init order:
    // 1. Init map font
    // 2. Get user position.
    // 3. THEN get closests bakeries
    // 4. Stylish the bakeries.
    console.log(options);
    var event = new CustomEvent('mapready');

    //GEOLOC STUFF
    function onLocationFound(e) {
        var radius = e.accuracy / 2;
        console.log(e.latlng)
        L.marker(e.latlng).addTo(map)
            // L.circle(e.latlng, radius).addTo(map);
    }


    map.on('locationfound', onLocationFound);
    map.locate({
        setView: true,
        watch: false,
        maxZoom: 16
    });

    map.addEventListener('mapready', insert_closest_bakeries_json(map, dataurl), false);

}