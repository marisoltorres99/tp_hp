var modalCancelar = document.getElementById("ModalCancelar");

modalCancelar.addEventListener("show.bs.modal", function (event) {
  // Obtengo el elemento (boton) que disparo el evento que hace aparecer al modal
  var button = event.relatedTarget;
  // Obtengo la informacion de los atributos del boton
  var reserva_id = button.getAttribute("clubpad-reserva-id");
  var reserva_fh = button.getAttribute("clubpad-reserva-fecha-hora");

  var boton_confirmar = document.getElementById("boton_confirmar");
  boton_confirmar.setAttribute("value", reserva_id);

  var modalTitle = modalCancelar.querySelector(".modal-title");

  modalTitle.textContent =
    "¿Desea cancelar la reserva del " + reserva_fh + " ?";
});
