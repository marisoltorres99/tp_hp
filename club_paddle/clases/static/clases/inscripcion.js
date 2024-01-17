var modalInscribir = document.getElementById("ModalInscribir");

modalInscribir.addEventListener("show.bs.modal", function (event) {
  // Obtengo el elemento (boton) que disparo el evento que hace aparecer al modal
  var button = event.relatedTarget;
  // Obtengo la informacion de los atributos del boton
  var boton_estado = button.getAttribute("clubpad-boton-estado-inscripcion");
  var insc_id = button.getAttribute("clubpad-user-id");

  var boton_confirmar = document.getElementById("boton_confirmar");
  boton_confirmar.setAttribute("value", insc_id);
  boton_confirmar.setAttribute("name", boton_estado);

  var modalTitle = modalInscribir.querySelector(".modal-title");

  boton_confirmar.setAttribute("class", "btn btn-success");
  boton_confirmar.textContent = "Confirmar";
  modalTitle.textContent = "¿Desea inscribirse a la clase ?";
});
