/* Zenodo's viewport is limited to under 800px, which makes it harder to fill some forms. */

document.getElementById("rdm-deposit-form").style.width = "90%"
[...document.getElementsByClassName("ui container")].forEach(e => e.style.width = "90%")
