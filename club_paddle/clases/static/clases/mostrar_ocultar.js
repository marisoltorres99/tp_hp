function mostrar_ocultar_select(idSelect, idRadio) {
  var select = document.getElementById(idSelect);
  var radio = document.getElementById(idRadio);
  if (radio.checked) {
    select.style.display = "inline";
  } else {
    select.style.display = "none";
  }
}
