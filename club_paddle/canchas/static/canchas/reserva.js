var modalReservar = document.getElementById("ModalReservar");

modalReservar.addEventListener("show.bs.modal", function (event) {
  // Obtengo el elemento (boton) que disparo el evento que hace aparecer al modal
  var button = event.relatedTarget;
  // Obtengo la informacion de los atributos del boton
  var cancha_id = button.getAttribute("clubpad-cancha-id");
  var fecha = button.getAttribute("clubpad-fecha");
  var hora = button.getAttribute("clubpad-hora");

  var boton_confirmar = document.getElementById("boton_confirmar");
  boton_confirmar.setAttribute("value", cancha_id);

  var input_fecha = document.getElementById("input_fecha");
  input_fecha.setAttribute("value", fecha);

  var input_hora = document.getElementById("input_hora");
  input_hora.setAttribute("value", hora);

  var modalTitle = modalReservar.querySelector(".modal-title");

  boton_confirmar.setAttribute("class", "btn btn-primary");
  boton_confirmar.textContent = "Confirmar";
  modalTitle.textContent =
    "¿Desea realizar la reserva: " +
    fecha +
    " " +
    hora +
    " Cancha " +
    cancha_id +
    " ?";
});
