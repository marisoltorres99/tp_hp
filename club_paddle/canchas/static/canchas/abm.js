var modalEstadoCancha = document.getElementById("ModalEstadoCancha");

modalEstadoCancha.addEventListener("show.bs.modal", function (event) {
  // Obtengo el elemento (boton) que disparo el evento que hace aparecer al modal
  var button = event.relatedTarget;
  // Obtengo la informacion de los atributos del boton
  var boton_estado = button.getAttribute("clubpad-boton-estado-cancha");
  var cancha_id = button.getAttribute("clubpad-cancha-id");
  var cancha_numero = button.getAttribute("clubpad-cancha-numero");

  var boton_confirmar = document.getElementById("boton_confirmar");
  boton_confirmar.setAttribute("value", cancha_id);
  boton_confirmar.setAttribute("name", boton_estado);

  var modalTitle = modalEstadoCancha.querySelector(".modal-title");

  if (boton_estado == "activar") {
    boton_confirmar.setAttribute("class", "btn btn-success");
    boton_confirmar.textContent = "Activar";
    modalTitle.textContent = "¿Desea activar la cancha " + cancha_numero + "?";
  } else {
    boton_confirmar.setAttribute("class", "btn btn-danger");
    boton_confirmar.textContent = "Desactivar";
    modalTitle.textContent =
      "¿Desea desactivar la cancha " + cancha_numero + "?";
  }
});
