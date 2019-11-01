var stars_radios = document.getElementsByClassName("gout_stars_radio");

var current_bakerie_id = null;

/* Set the width of the side navigation to 250px */
function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

/* Set the width of the side navigation to 0 */
function closeNav() {
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

}

function formSubmit() {
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

    fetch(post_url, myInit).then(
        function(response) {
            return response
        }).catch(err =>
        console.log(err)
    )
}

for (let rad of stars_radios) {
    rad.addEventListener("click", function() { console.log(document.querySelector('input[name="stars_gout"]:checked').value) })

}