var modalEstadoClase = document.getElementById("ModalEstadoClase");

modalEstadoClase.addEventListener("show.bs.modal", function (event) {
  // Obtengo el elemento (boton) que disparo el evento que hace aparecer al modal
  var button = event.relatedTarget;
  // Obtengo la informacion de los atributos del boton
  var boton_estado = button.getAttribute("clubpad-boton-estado-clase");
  var clase_id = button.getAttribute("clubpad-clase-id");

  var boton_confirmar = document.getElementById("boton_confirmar");
  boton_confirmar.setAttribute("value", clase_id);
  boton_confirmar.setAttribute("name", boton_estado);

  var modalTitle = modalEstadoClase.querySelector(".modal-title");

  if (boton_estado == "activar") {
    boton_confirmar.setAttribute("class", "btn btn-success");
    boton_confirmar.textContent = "Activar";
    modalTitle.textContent = "¿Desea activar la clase " + clase_id + "?";
  } else {
    boton_confirmar.setAttribute("class", "btn btn-danger");
    boton_confirmar.textContent = "Desactivar";
    modalTitle.textContent = "¿Desea desactivar la clase " + clase_id + "?";
  }
});
