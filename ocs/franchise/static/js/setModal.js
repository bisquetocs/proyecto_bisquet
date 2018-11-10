function update_private_product(product_id) {
  product_title = document.getElementById("product_title");
  product_selected = document.getElementById("product_"+product_id);

  product_title.innerHTML = product_selected.innerHTML;
  document.getElementById("id_product_to_change").value = product_id
}

function change_to_input_text() {
  console.log("hue")
  document.getElementById("io_text").innerHTML = "Cantidad que será ingresada.";
}

function change_to_output_text() {
  document.getElementById("io_text").innerHTML = "Cantidad que será retirada.";
}
