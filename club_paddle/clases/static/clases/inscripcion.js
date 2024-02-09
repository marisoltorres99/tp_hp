var modalInscribir = document.getElementById("ModalInscribir");

modalInscribir.addEventListener("show.bs.modal", function (event) {
  // Obtengo el elemento (boton) que disparo el evento que hace aparecer al modal
  var button = event.relatedTarget;
  // Obtengo la informacion de los atributos del boton
  var clase_id = button.getAttribute("clubpad-clase-id");
  var profesor = button.getAttribute("clubpad-clase-profesor");
  var desc = button.getAttribute("clubpad-clase-desc");
  var cancha = button.getAttribute("clubpad-clase-cancha");

  var boton_confirmar = document.getElementById("boton_confirmar");
  boton_confirmar.setAttribute("value", clase_id);

  var modalTitle = modalInscribir.querySelector(".modal-title");

  modalTitle.textContent =
    "¿Desea inscribirse a la Clase: " +
    clase_id +
    " Prof: " +
    profesor +
    " Desc: " +
    desc +
    " Cancha: " +
    cancha +
    "?";
});
