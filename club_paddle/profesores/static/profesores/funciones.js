var modalEstadoProfesor = document.getElementById("ModalEstadoProfesor");

modalEstadoProfesor.addEventListener("show.bs.modal", function (event) {
  // Obtengo el elemento (boton) que disparo el evento que hace aparecer al modal
  var button = event.relatedTarget;
  // Obtengo la informacion de los atributos del boton
  var boton_estado = button.getAttribute("clubpad-boton-estado-profe");
  var profe_id = button.getAttribute("clubpad-profe-id");
  var profe_nombre = button.getAttribute("clubpad-profe-nombre");

  var boton_confirmar = document.getElementById("boton_confirmar");
  boton_confirmar.setAttribute("value", profe_id);
  boton_confirmar.setAttribute("name", boton_estado);

  var modalTitle = modalEstadoProfesor.querySelector(".modal-title");

  if (boton_estado == "activar") {
    boton_confirmar.setAttribute("class", "btn btn-success");
    boton_confirmar.textContent = "Activar";
    modalTitle.textContent = "¿Desea activar al profesor " + profe_nombre + "?";
  } else {
    boton_confirmar.setAttribute("class", "btn btn-danger");
    boton_confirmar.textContent = "Desactivar";
    modalTitle.textContent =
      "¿Desea desactivar al profesor " + profe_nombre + "?";
  }
});
