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
        // 2. Update form
    document.getElementById("enseigne").value = properties.enseigne
    document.getElementById("commentaire").value = properties.commentaire
    document.getElementsByName("stars").value = 1
}

function slot_empty_map_clicked() {
    // 1. Delete forms
    // 2. Hide pannel

}