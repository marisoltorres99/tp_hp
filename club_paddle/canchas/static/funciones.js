function mostrar_input_hora(id, hora_id) {
  var checkBox = document.getElementById(id);
  var input_hora = document.getElementById(hora_id);
  if (checkBox.checked == true) {
    input_hora.style.display = "inline";
  } else {
    input_hora.style.display = "none";
  }
}
