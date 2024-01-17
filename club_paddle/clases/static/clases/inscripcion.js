var modalInscribir = document.getElementById("ModalInscribir");

modalInscribir.addEventListener("show.bs.modal", function (event) {
  // Obtengo el elemento (boton) que disparo el evento que hace aparecer al modal
  var button = event.relatedTarget;
  // Obtengo la informacion de los atributos del boton
  var clase_id = button.getAttribute("clubpad-clase-id");

  var boton_confirmar = document.getElementById("boton_confirmar");
  boton_confirmar.setAttribute("value", clase_id);

  var modalTitle = modalInscribir.querySelector(".modal-title");

  boton_confirmar.setAttribute("class", "btn btn-primary");
  boton_confirmar.textContent = "Confirmar";
  modalTitle.textContent = "¿Desea inscribirse a la clase " + clase_id + " ?";
});
