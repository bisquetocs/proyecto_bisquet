// AJAX SETUP --------------------START
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
// AJAX SETUP --------------------END

function con(message){
  console.log(message);
}
function doc(id){
  return document.getElementById(id);
}
function removeElement(elementId) {
  var element = doc(elementId);
  element.parentNode.removeChild(element);
}
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

$(document).keypress(function(e) {
    if(e.which == 13) {
      switch(document.activeElement){
        case doc('add_product'):
          if(doc('add_product').value == 0 ||
                                    doc('add_product').value == null){
              document.activeElement= doc('add_product');
              doc('add_product').focus();
          }else{
            document.activeElement= doc('ud_medida');
            doc('ud_medida').focus();
          }
        break;
        case doc('cantidad_pedida'):
          if(doc('cantidad_pedida').value == 0 ||
                                    doc('cantidad_pedida').value == null){
              document.activeElement= doc('cantidad_pedida');
              doc('cantidad_pedida').focus();
          }else{
            document.activeElement= doc('add_product_button');
            doc('add_product_button').focus();
          }
          add_product_to_order();
        break;
        case doc('add_product_button'):
          //FUNCION PARA AGREGAR PRODUCTO
          //add_product_to_order();
        break;
      }
    }
});

function check_product_unidad(aux){
  doc('ud_medida').innerHTML = '';
  doc('ud_medida').disabled = true;
  doc('cantidad_pedida').disabled = true;
  id_provider = doc('orderProvider').value;
  nombre_product = doc('add_product').value;
  if(nombre_product != '' && nombre_product != null && nombre_product != ' '){
    $.ajax({
      url: '/products/check_available_product/',
      data: {
        'id_provider': id_provider,
        'nombre_product': nombre_product,
      },
      dataType: 'json',
      type: 'GET',
      success: function(data) {
        if(data.error){
          if(aux){
            alert(doc('orderProvider').name+' no está vendiendo un producto llamado '+nombre_product);
            doc('add_product').value = '';
          }
        }else{
          doc('ud_medida').disabled = false;
          doc('cantidad_pedida').disabled = false;
          string = '';
          for(var i=0; i< data.id_unidades.length; i++){
            string += '<option value="'+data.id_unidades[i]+'">'+data.unidades[i]+'</option>';
          }
          if(string!=doc('ud_medida').innerHTML){
            doc('ud_medida').innerHTML = string;
          }
        }
      }
    });
  }else{
    doc('add_product').value = '';
  }
}
function activate_add_button(){
  if(doc('cantidad_pedida').value!=0 && doc('cantidad_pedida').value!=null){
    doc('add_product_button').disabled = false;
  }else if(doc('cantidad_pedida').value==null || doc('cantidad_pedida').value==0){
    doc('add_product_button').disabled = true;
  }

}

function add_product_to_order(){
  if (doc('fecha_ideal').value != null){
    var date = new Date(doc('fecha_ideal').value);
    var dd = date.getDate();
    var mm = date.getMonth()+1; //January is 0!
    var yyyy = date.getFullYear();
     if(dd<10){
       dd='0'+dd;
     }
     if(mm<10){
       mm='0'+mm;
     }
    date = yyyy+'-'+mm+'-'+dd;
    if(doc('add_product').value != null){
      if(doc('ud_medida').value != 0){
        if(doc('cantidad_pedida').value != null && doc('cantidad_pedida').value != 0){
          doc('enviar_pedido').disabled = true;
          $.ajax({
             url: '/orders/add_product_to_order/',
             data: {
               'id_pedido': doc('id_pedido').value,
               'id_provider': doc('orderProvider').value,
               'nombre_producto': doc('add_product').value,
               'ud_medida': doc('ud_medida').value,
               'cantidad_pedida': doc('cantidad_pedida').value,
               'date': date,
             },
             dataType: 'json',
             type: 'GET',
             success: function(data) {
               if(data.success){
                 if (doc('edited').value == 0){
                   doc('edited').value = 1;
                   doc('contenido_pedido').innerHTML = '<tr id="row'+data.id_ord_prod+'" scope="row">'+
                                                         '<td>'+data.cantidad+'</td>'+
                                                         '<td>'+data.ud_medida+'</td>'+
                                                         '<td>'+capitalizeFirstLetter(data.producto)+'</td>'+
                                                         '<td>$ '+data.precio+'</td>'+
                                                         '<td>$ '+data.total+'</td>'+
                                                         '<td>'+
                                                           '<button type="button" class="btn btn-sm btn-outline-danger" name="button" onclick="delete_product_from_order('+data.id_ord_prod+')">'+
                                                             '<span class="fa fa-trash"></span>'+
                                                           '</button>'+
                                                         '</td>'+
                                                       '</tr>';
                 }else{
                   if(doc("row"+data.id_ord_prod)){
                     removeElement("row"+data.id_ord_prod);
                   }
                   doc('contenido_pedido').innerHTML += '<tr id="row'+data.id_ord_prod+'" scope="row">'+
                                                         '<td>'+data.cantidad+'</td>'+
                                                         '<td>'+data.ud_medida+'</td>'+
                                                         '<td>'+data.producto+'</td>'+
                                                         '<td>$ '+data.precio+'</td>'+
                                                         '<td>$ '+data.total+'</td>'+
                                                         '<td>'+
                                                           '<button type="button" class="btn btn-sm btn-outline-danger" name="button" onclick="delete_product_from_order('+data.id_ord_prod+')">'+
                                                             '<span class="fa fa-trash"></span>'+
                                                           '</button>'+
                                                         '</td>'+
                                                       '</tr>';
                 }
                 doc('total_productos').value = data.cantidad_total;
                 doc('total_precio').value = data.precio_total;
                 doc('id_pedido').value = data.id_pedido;
                 doc('add_product').value = null;
                 doc('cantidad_pedida').value = null;
                 doc('enviar_pedido').disabled = false;
                 doc('ud_medida').innerHTML = '';
                 doc('ud_medida').disabled = true;
                 doc('cantidad_pedida').disabled = true;
               }
               removeElement('product'+data.id_product);
               doc('enviar_pedido_card').hidden = false;
             }
          });
        }else{
          alert('No has llenado los campos necesarios!');
        }
      }else{
        alert('No has llenado los campos necesarios!');
      }
    }else{
      alert('No has llenado los campos necesarios!');
    }
  }else{
    alert('Registra una fecha para tu pedido');
  }
}

function calculate_day(){
  var date = new Date(doc('fecha_ideal').value);
  var n = date.getDay();
  switch(n){
    case 0:doc('dia_ideal').value = 'LUNES';break;
    case 1:doc('dia_ideal').value = 'MARTES';break;
    case 2:doc('dia_ideal').value = 'MIÉRCOLES';break;
    case 3:doc('dia_ideal').value = 'JUEVES';break;
    case 4:doc('dia_ideal').value = 'VIERNES';break;
    case 5:doc('dia_ideal').value = 'SÁBADO';break;
    case 6:doc('dia_ideal').value = 'DOMINGO';break;
  }
  doc('add_product').disabled = false;
  doc('add_product').focus();
  //alert(Date.getDate());
}

function start_order(){
  doc('realizar_pedido').hidden = true;
  doc('fecha_ideal').focus()
}
function edit_order(){
  doc('editar_pedido').hidden = true;
  doc('enviar_pedido').hidden = false;
  doc('add_product').disabled = false;
  doc('add_product').focus()
}

function delete_product_from_order(id_prod_ord){
  if(confirm('Seguro que quieres eliminar este producto de tu pedido?')){
    doc('enviar_pedido').disabled = true;
    $.ajax({
       url: '/orders/delete_product_from_order/',
       data: {
         'id_pedido': doc('id_pedido').value,
         'id_provider': doc('orderProvider').value,
         'id_prod_ord': id_prod_ord,
       },
       dataType: 'json',
       type: 'GET',
       success: function(data) {
         if(data.success){
           removeElement('row'+id_prod_ord);
           doc('enviar_pedido').disabled = false;
           doc('list_products').innerHTML = doc('list_products').innerHTML+'<option id="product'+data.id_product+'" name="'+data.id_product+'" value="'+data.nombre_product+'">';
           doc('total_productos').value = data.cantidad_total;
           doc('total_precio').value = data.precio_total;
         }
       }
    });
  }


}


function cancel_order(){
  if(confirm('¿Seguro que quieres cancelar este pedido? ¡Esta acción no tiene regreso!')){
    $.ajax({
      url: '/orders/cancel_order/',
      data: {
        'id_pedido': doc('id_pedido').value,
        'id_provider': doc('orderProvider').value,
      },
      dataType: 'json',
      type: 'GET',
      success: function(data) {
        alert('El pedido ha sido cancelado');
        location.reload();
      }
    });
  }
}
function send_order(){
  if(confirm('¿Seguro que quieres enviar este pedido? ¡El proveedor ya podrá ver el contenido y las actualizaciones que vayas haciendo!')){
    $.ajax({
      url: '/orders/send_order/',
      data: {
        'id_pedido': doc('id_pedido').value,
        'id_provider': doc('orderProvider').value,
      },
      dataType: 'json',
      type: 'GET',
      success: function(data) {
        alert('El pedido ha sido enviado');
        location.reload();
      }
    });
  }
}









//
