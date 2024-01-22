var modalDesactivarCuenta = document.getElementById("ModalDesactivarCuenta");

modalDesactivarCuenta.addEventListener("show.bs.modal", function (event) {
  // Obtengo el elemento (boton) que disparo el evento que hace aparecer al modal
  var button = event.relatedTarget;
  // Obtengo la informacion de los atributos del boton
  var user_id = button.getAttribute("clubpad-user-id");

  var boton_confirmar = document.getElementById("boton_confirmar");
  boton_confirmar.setAttribute("value", user_id);

  var modalTitle = modalDesactivarCuenta.querySelector(".modal-title");

  boton_confirmar.setAttribute("class", "btn btn-danger");
  boton_confirmar.textContent = "Desactivar";
  modalTitle.textContent = "Ingrese su contraseña para desactivar la cuenta";
});
