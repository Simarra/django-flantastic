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

    document.getElementsByName("stars").value = 1
}

function slot_empty_map_clicked() {
    // 1. Delete forms
    // 2. Hide pannel

}

// TODO: Add an event listener on start system

function star_rating() {

}

var taste_value = 0;

var radios = document.getElementsByName("stars");

for (let rad of radios) {
    console.log("hi hi")
    rad.addEventListener("click", function() { console.log(document.querySelector('input[name="stars"]:checked').value) })

}