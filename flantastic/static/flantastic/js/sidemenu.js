var stars_radios = document.getElementsByClassName("gout_stars_radio");

var current_bakerie_id = null;
var current_bakerie_global_note = null;

/* Set the width of the side navigation to 250px */
function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

/* Set the width of the side navigation to 0 */
function closeNav() {
    // Reset all fields and hide the pannel
    document.getElementById("enseigne").value = null;
    document.getElementById("commentaire").value = null;
    // set the id of bakerie in a global variable to get it later.
    current_bakerie_id = null;
    current_bakerie_global_note = null;


    let stars_elts = ["gout", "apparence", "pate", "texture"]
    for (let star_elt of stars_elts) {
        let current_elt = document.getElementsByName("stars_" + star_elt)
        for (let rad of current_elt) {
            rad.checked = false;
        }
    }
    document.getElementById("mySidenav").style.width = "0";
}


function slot_markup_clicked(properties) {
    // 1. Show pannel
    openNav()
        // 3. Update form
    document.getElementById("enseigne").value = properties.enseigne;
    document.getElementById("commentaire").value = properties.commentaire;
    // set the id of bakerie in a global variable to get it later.
    current_bakerie_id = properties.pk;


    let stars_elts = ["gout", "apparence", "pate", "texture"]
    for (let star_elt of stars_elts) {
        if (properties[star_elt] === null) {
            let current_elt = document.getElementsByName("stars_" + star_elt)
            for (let rad of current_elt) {
                rad.checked = false;
            }
        } else {
            document.getElementById(star_elt + properties[star_elt]).checked = true;
        }
    }
}

function slot_empty_map_clicked() {
    // 1. Delete forms
    // 2. Hide pannel
    closeNav()

}

async function formSubmit() {
    // Event triggered when the user submit  form

    // generate headers and get data to transmit
    let data = JSON.stringify({
        enseigne: document.getElementById("enseigne").value,
        commentaire: document.getElementById("commentaire").value,
        gout: document.querySelector('input[name="stars_gout"]:checked').value,
        apparence: document.querySelector('input[name="stars_apparence"]:checked').value,
        texture: document.querySelector('input[name="stars_texture"]:checked').value,
        pate: document.querySelector('input[name="stars_pate"]:checked').value,
        pk: current_bakerie_id,
        csrfmiddlewaretoken: document.querySelector('input[name=csrfmiddlewaretoken]').value,
        action: 'post'
    });

    let myInit = {
        method: 'POST',
        body: data,
        credentials: 'same-origin',
        headers: { "X-CSRFToken": document.querySelector('input[name=csrfmiddlewaretoken]').value },
    };

    // Post the data and get the result
    try {
        let res_json = await fetch(post_url, myInit)
        var res = await res_json.json()
    } catch {
        console.log("error")
    }

    refresh_updated_point(res);
    closeNav()



}


function refresh_updated_point(bak_data) {
    // Method used to refresh the point properties in the map

    // Get the updated point
    let bak_leaflet_id = get_bakerie_from_gjson(bak_data.pk);
    gjson.features[bak_leaflet_id].properties.enseigne = bak_data.enseigne;
    gjson.features[bak_leaflet_id].properties.commentaire = bak_data.commentaire;
    gjson.features[bak_leaflet_id].properties.gout = bak_data.gout;
    gjson.features[bak_leaflet_id].properties.apparence = bak_data.apparence;
    gjson.features[bak_leaflet_id].properties.texture = bak_data.texture;
    gjson.features[bak_leaflet_id].properties.pate = bak_data.pate;
    gjson.features[bak_leaflet_id].properties.global_note = bak_data.global_note;

}


function get_bakerie_from_gjson(bakerie_id) {
    // Extract bakerie id from gjson;
    for (let the_id in gjson.features) {
        if (parseInt(gjson.features[the_id].properties.pk) == parseInt(bakerie_id)) {
            return the_id;
        }
    }
    throw new Error("Bakerie not found")

}