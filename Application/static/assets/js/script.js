//==============================PAGE D'ACCUEIL ===================================================//
// Get the Sidebar
var mySidebar = document.getElementById("mySidebar");

// Get the DIV with overlay effect
var overlayBg = document.getElementById("myOverlay");

// Toggle between showing and hiding the sidebar, and add overlay effect
function w3_open() {
  if (mySidebar.style.display === 'block') {
    mySidebar.style.display = 'none';
    overlayBg.style.display = "none";
  } else {
    mySidebar.style.display = 'block';
    overlayBg.style.display = "block";
  }
}

// Close the sidebar with the close button
function w3_close() {
  mySidebar.style.display = "none";
  overlayBg.style.display = "none";
}

function myFunc(id) {
  var x = document.getElementById(id);
  if (x.className.indexOf("w3-show") == -1) {
    x.className += " w3-show"; 
    x.previousElementSibling.className += " w3-ligth-red";
  } else { 
    x.className = x.className.replace(" w3-show", "");
    x.previousElementSibling.className = 
    x.previousElementSibling.className.replace(" w3-ligth-red", "");
  }
}

//======================================PAGE DU PERSONNEL =========================================//
//Fonction de filtre du tableau du personnel 
function filterTable() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("searchInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  var filterType = document.getElementById("filterMatriculeSexe").value;

  for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[filterType === "sexe" ? 2 : 0];
      if (td) {
          txtValue = td.textContent || td.innerText;
          if (txtValue.toUpperCase().indexOf(filter) > -1 || filterType === "all") {
              tr[i].style.display = "";
          } else {
              tr[i].style.display = "none";
          }
      }
  }
}

//Formulaire d'ajout d'un personnel 
//Modal de deconnexion
function OpenModal(){
  document.getElementById('idDeconnexion').style.display='block'
}
function CloseModal(){
  document.getElementById('idDeconnexion').style.display = 'none'
}
