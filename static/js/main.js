// Desplegar y contraer el menú princupal en mobile
const navBtnToggle = document.querySelector(".nav-btn-toggle");
const navMenu = document.querySelector(".menu");

navBtnToggle.addEventListener("click", () => {
   navMenu.classList.toggle("menu-visible");

   if (navMenu.classList.contains("menu-visible")) {
      navBtnToggle.setAttribute("aria-label", "Cerrar menú");
   } else {
      navBtnToggle.setAttribute("aria-label", "Abrir menú");
   }
});

// Desplegar y contraer elementos del submenú en mobile
const dropDown = document.getElementsByClassName("dropdown-item");

for (let i = 0; i < dropDown.length; i++) {
   dropDown[i].addEventListener("click", function() {
      this.classList.toggle("open");
   });
}