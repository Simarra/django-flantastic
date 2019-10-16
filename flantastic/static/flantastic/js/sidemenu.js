var radios = document.getElementsByName("stars");

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

    if (properties.gout === null) {
        for (let rad of radios) {
            rad.checked = false;
        }
    } else {
        document.getElementById('gout' + properties.gout).checked = true;
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

for (let rad of radios) {
    rad.addEventListener("click", function() { console.log(document.querySelector('input[name="stars"]:checked').value) })

}