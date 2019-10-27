var stars_radios = document.getElementsByClassName("gout_stars_radio");

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
    document.getElementById("enseigne").value = properties.enseigne
    document.getElementById("commentaire").value = properties.commentaire


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
    var myInit = {
        method: 'POST',
        // headers: myHeaders,
        data: {
            enseigne: document.getElementById("enseigne").value,
            commentaire: document.getElementById("commentaire").value,
            gout: document.querySelector('input[name="stars"]:checked').value,
            csrfmiddlewaretoken: document.querySelector('input[name=csrfmiddlewaretoken]').value,
            action: 'post'
        }
    };
    fetch(post_url, myInit).then(
        function(response) {
            return response.blob()
        })
}

for (let rad of stars_radios) {
    rad.addEventListener("click", function() { console.log(document.querySelector('input[name="stars_gout"]:checked').value) })

}