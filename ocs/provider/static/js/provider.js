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

// INITIAL FUNCTIONS
$( document ).ready(function() {
  // DATA TABLES
    $('#myTable').DataTable({
      "language": {
            "lengthMenu": "Mostrar _MENU_ elementos por página",
            "zeroRecords": "No se encontraron resultados",
            "info": "Página _PAGE_ de _PAGES_",
            "infoEmpty": "No hay registros disponibles",
            "infoFiltered": "(filtered from _MAX_ total records)",
            "search":         "Buscar:",
            "paginate": {
                "first":      "Primero",
                "last":       "Último",
                "next":       "Siguiente",
                "previous":   "Anterior"
            },
        }
    });
});


function con(aux){
  console.log(aux);
}
function doc(aux){
  return document.getElementById(aux);
}
// EXTRA (LITTLE USE BUT NO USELESS)
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

// ADD OR EDIT PRODUCT (INFO AND PRICES)
function editProduct(id_product){
  cancelAgregar();
  //INFO GENERAL DEL PRODUCTO
  doc('editar_producto').hidden = false;
  doc('agregar_producto').hidden = true;
  doc('no_selected').hidden = true;
  doc('selected').hidden = false;
  //PRECIOS
  doc('selected_price').hidden = false;
  doc('no_selected_price').hidden = true;
  doc('adding_price').hidden = true;
  //EQUIVALENCIAS
  doc('selected_equiv').hidden = false;
  doc('no_selected_equiv').hidden = true;
  doc('adding_equiv').hidden = true;
  //SELECTS AND OTHERS
  doc('unidad_de_medida').value = 0;
  doc('price').value = null;
  doc('cantidad_origen').disabled=true;
  doc('cantidad_origen').value= 1;
  doc('unidad_origen').value = 0;
  doc('unidad_destino').value = 0;
  doc('unidad_destino').disabled = true;
  doc('cantidad_destino').value = null;
  var id_product = id_product;
  $.ajax({
     url: '/products/get_product/',
     data: {
        'id_product': id_product
     },
     dataType: 'json',
     type: 'GET',
     success: function(data) {
       doc('id_product').value = data.id_product;
       document.getElementsByClassName('nombre_producto');
       list = document.getElementsByClassName('nombre_producto');
       for(var i=0; i<list.length; i++){
         list[i].innerHTML = capitalizeFirstLetter(data['nombre']);
       }
       doc('nombre').value = capitalizeFirstLetter(data['nombre']);
       doc('descripcion').innerHTML = data.descripcion;
       doc('codigo').value = data.codigo;
       doc('activo').checked = data.activo;
       checaUnidad();
     }
  });
  $.ajax({
     url: '/products/get_product_price/',
     data: {
        'id_product': id_product
     },
     dataType: 'json',
     type: 'GET',
     success: function(data) {
       doc('id_product').value = data.id_product;
       doc('precios_de_producto').innerHTML = '<div class="col-5"><h6>Unidad de medida:</h6></div>'+
                                                    '<div class="col-4"><h6>Precio:</h6></div>'+
                                                    '<div class="col-3"></div>';
       for(var i=0; i<data.id_unidad.length; i++){
         doc('precios_de_producto').innerHTML = doc('precios_de_producto').innerHTML +
         '<div class="col-5"><input required id="uni'+data.id_precio[i]+'" name="'+data.id_unidad[i]+'" type="text" class="form-control" value="'+data.unidad[i]+'" disabled></div>'+
         '<div class="col-5"><input required id="pre'+data.id_precio[i]+'" name="" type="number" class="form-control" value="'+data.precio[i]+'" min="0" step="0.01" disabled></div>'+

         '<div class="col-2 align-self-center">'+
         '<button id="editThisPrice'+data.id_precio[i]+'" type="button" class="btn btn-sm " name="button" onclick="editThisPrice('+data.id_precio[i]+')">'+
           '<span class="fa fa-edit"></span>'+
         '</button>'+
         '<div id="editThisPriceSection'+data.id_precio[i]+'" hidden class="btn-group" role="group" aria-label="Basic example">'+
           '<button type="button" class="btn btn-sm btn-secondary" name="button" onclick="cancelPrice('+data.id_precio[i]+')">'+
             '<span class="fa fa-remove"></span>'+
           '</button>'+
           '<button type="button" class="btn btn-sm btn-success" name="button" onclick="savePrice('+data.id_precio[i]+')">'+
             '<span class="fa fa-hdd-o"></span>'+
           '</button>'+
           '<button type="button" class="btn btn-sm btn-danger" name="button" onclick="deleteThisPrice('+data.id_precio[i]+')">'+
             '<span class="fa fa-trash"></span>'+
           '</button>'+
         '</div></div>';
       }
     }
  });
  $.ajax({
     url: '/products/get_product_equiv/',
     data: {
        'id_product': id_product,
     },
     dataType: 'json',
     type: 'GET',
     success: function(data) {
       doc('equivalencias_de_producto').innerHTML = '<br />'+
                                               '<p style="color:gray">'+
                                                'Aún no registras ninguna equivalencia'+
                                               '</p>'+
                                               '<br /><br />';
       if(data){
         for(var i=0; i<data.id_unidad_total.length; i++){
           doc('optuniorg'+data.id_unidad_total[i]).hidden = true;
         }
         for(var i=0; i<data.id_unidad_posible.length; i++){
           doc('optuniorg'+data.id_unidad_posible[i]).hidden = false;
         }
         if(data.id_unidad_origen.length!=0){
           doc('equivalencias_de_producto').innerHTML = '';
           for(var i=0; i<data.id_unidad_origen.length; i++){
             doc('equivalencias_de_producto').innerHTML = doc('equivalencias_de_producto').innerHTML+
                                                  '<li class="list-group-item clearfix" onmouseover="showDeleteEquiv('+data.id_equiv[i]+')"  onmouseout="hideDeleteEquiv('+data.id_equiv[i]+')">'+
                                                  '<div class="float-left">'+
                                                  data.cantidad_origen[i]+' '+
                                                  data.id_unidad_origen[i]+' = '+
                                                  data.cantidad_destino[i]+' '+
                                                  data.id_unidad_destino[i]+
                                                  '</div>'+
                                                  '<div class="float-right">'+
                                                  '<button hidden id="equiv'+data.id_equiv[i]+'" type="button" class="btn btn-sm btn-danger" name="button" onclick="delete_equiv('+data.id_equiv[i]+')">'+
                                                    '<span class="fa fa-trash"></span>'+
                                                  '</button>'+
                                                  '</div>'+
                                                  '</li>';
           }
         }
       }
     }
  });
}

function cancelEdit(){
  //PRICE
  doc('selected_price').hidden = true;
  doc('no_selected_price').hidden = false;
  doc('adding_price').hidden = true;
  //EQUIVALENCIAS
  doc('selected_equiv').hidden = true;
  doc('no_selected_equiv').hidden = false;
  doc('adding_equiv').hidden = true;
  //INFO GENERAL DEL PRODUCTO
  doc('editar_producto').hidden = false;
  doc('selected').hidden = true;
  doc('no_selected').hidden = false;
  doc('agregar_producto').hidden = true;
  //OTHERS
  doc('id_product').value = '';
  doc('nombre').value = '';
  doc('descripcion').innerHTML = '';
  doc('codigo').value = '';
  doc('cantidad_origen').disabled=true;
  //doc('activo').checked = True;
  doc('precios_de_producto').innerHTML = ' ';
  list = document.getElementsByClassName('nombre_producto');
  for(var i=0; i<list.length; i++){
    list[i].innerHTML = '';
  }
}

function showAgregar(){
  cancelEdit();
  doc('selected_price').hidden = true;
  doc('no_selected_price').hidden = true;
  doc('adding_price').hidden = false;

  doc('selected_equiv').hidden = true;
  doc('no_selected_equiv').hidden = true;
  doc('adding_equiv').hidden = false;

  doc('editar_producto').hidden = true;
  doc('agregar_producto').hidden = false;
}

function cancelAgregar(){
  //PRICE
  doc('selected_price').hidden = true;
  doc('no_selected_price').hidden = false;
  doc('adding_price').hidden = true;
  //EQUIV
  doc('selected_equiv').hidden = true;
  doc('no_selected_equiv').hidden = false;
  doc('adding_equiv').hidden = true;
  //INFO GENERAL
  doc('editar_producto').hidden = false;
  doc('selected').hidden = true;
  doc('no_selected').hidden = false;
  doc('agregar_producto').hidden = true;
  //OTHERS
  doc('nombre').value = '';
  doc('descripcion').innerHTML = '';
  doc('codigo').value = '';
}

function ableUnable(id_product){
  doc('ableUnable'+id_product).innerHTML = '<div style="color:gary">'+
                                                               '<span class="fa fa-eye"></span>'+
                                                               '</div>';
  $.ajax({
     url: '/products/able_unable_product/',
     data: {
        'id_product': id_product
     },
     dataType: 'json',
     type: 'GET',
     success: function(data) {
       if(data.able){
         doc('ableUnable'+id_product).innerHTML = '<div style="color:green" onclick="ableUnable('+id_product+')">'+
                                                                      '<span class="fa fa-eye"></span>'+
                                                                      '</div>';
       }else{
         doc('ableUnable'+id_product).innerHTML = '<div style="color:red" onclick="ableUnable('+id_product+')">'+
                                                                      '<span class="fa fa-eye-slash"></span>'+
                                                                      '</div>';
       }
     }
  });
}
// PRODCUT PRICES
function checaUnidad(){
  var id_product = doc('id_product').value;
  if(id_product!=null){
    $.ajax({
       url: '/products/check_unidad/',
       data: {
          'id_product': id_product,
       },
       dataType: 'json',
       type: 'GET',
       success: function(data) {
         for(var i=0; i<data.unidadesTotal.length; i++){
           doc('optuni'+data.unidadesTotal[i]).disabled = false;
         }
         for(var i=0; i<data.unidades.length; i++){
           doc('optuni'+data.unidades[i]).disabled = true;
         }
       }
    });
  }
}

function addPrice(){
  var id_product = doc('id_product').value;
  var id_unidad = doc('unidad_de_medida').value;
  var cantidad = doc('price').value;
  if(cantidad > 0){
    $.ajax({
       url: '/products/add_price/',
       data: {
          'id_product': id_product,
          'id_unidad': id_unidad,
          'cantidad': cantidad,
       },
       dataType: 'json',
       type: 'GET',
       success: function(data) {
         editProduct(id_product);
       }
    });
  }
}

function editThisPrice(id_price){
  doc('pre'+id_price).disabled = false;
  doc('editThisPrice'+id_price).hidden = true;
  doc('editThisPriceSection'+id_price).hidden = false;
  doc('pre'+id_price).name = doc('pre'+id_price).value;
}

function deleteThisPrice(id_price){
  var producto = doc('nombre').value;
  var unidad = doc('uni'+id_price).value;
  var id_product = doc('id_product').value;
  var id_unidad = doc('uni'+id_price).name;
  if(confirm('¿Seguro que deseas dejar de vender '+producto+' en '+unidad+'?')){
    $.ajax({
       url: '/products/delete_price/',
       data: {
          'id_product': id_product,
          'id_unidad': id_unidad,
       },
       dataType: 'json',
       type: 'GET',
       success: function(data) {
         editProduct(id_product);
       }
    });
  }
  cancelPrice(id_price);
}

function savePrice(id_price){
  var id_product = doc('id_product').value;
  var id_unidad = doc('uni'+id_price).name;
  var cantidad = doc('pre'+id_price).value;
  if (doc('pre'+id_price).name != cantidad){
    $.ajax({
       url: '/products/save_price/',
       data: {
          'id_product': id_product,
          'id_unidad': id_unidad,
          'cantidad': cantidad,
       },
       dataType: 'json',
       type: 'GET',
       success: function(data) {
         doc('pre'+id_price).disabled = true;
         doc('editThisPrice'+id_price).hidden = false;
         doc('editThisPriceSection'+id_price).hidden = true;
         doc('pre'+id_price).value = cantidad;
         doc('pre'+id_price).name = cantidad;
       }
    });
  } else{
    cancelPrice(id_price);
  }
}

function cancelPrice(id_price){
  doc('pre'+id_price).disabled = true;
  doc('editThisPrice'+id_price).hidden = false;
  doc('editThisPriceSection'+id_price).hidden = true;
  doc('pre'+id_price).value = doc('pre'+id_price).name;
}

// PRODUCT EQUIVALENCIAS
function registrarEquivalencia(){
  var id_product = doc('id_product').value;
  var id_unidad_origen = doc('unidad_origen').value;
  var cantidad_origen = doc('cantidad_origen').value;
  var id_unidad_destino = doc('unidad_destino').value;
  var cantidad_destino = doc('cantidad_destino').value;
  var unidad_destino = doc('optunidest'+id_unidad_destino).innerHTML;

  if(cantidad_destino > 0 && cantidad_destino != null
        && cantidad_origen > 0 && cantidad_origen != null
        && id_unidad_origen!=0 && id_unidad_origen!=null
        && id_unidad_destino!=0 && id_unidad_destino!=null
        && id_unidad_destino!=id_unidad_origen){
    var also_price = false;
    //if(confirm('¿Deseas agregar el precio correspondiente para '+unidad_destino+' ?')){
    //  also_price = true;
    //}
    $.ajax({
       url: '/products/add_equivalencia/',
       data: {
          'id_product': id_product,
          'id_unidad_origen': id_unidad_origen,
          'cantidad_origen': cantidad_origen,
          'id_unidad_destino': id_unidad_destino,
          'cantidad_destino': cantidad_destino,
          //'also_price': also_price,
       },
       dataType: 'json',
       type: 'GET',
       success: function(data) {
         editProduct(id_product);
       }
    });
  }
}

function showDeleteEquiv(id_equiv){
  doc('equiv'+id_equiv).hidden = false;
}

function hideDeleteEquiv(id_equiv){
  doc('equiv'+id_equiv).hidden = true;
}

function delete_equiv(id_equiv){
  var id_product = doc('id_product').value;
  if(confirm('Seguro que deseas eliminar esta equivalencia?')){
    $.ajax({
       url: '/products/delete_equiv/',
       data: {
          'id_equiv': id_equiv,
       },
       dataType: 'json',
       type: 'GET',
       success: function(data) {
         editProduct(id_product);
       }
    });
  }
}

function checkEquivDestino(id_unidad_origen){
  var id_product = doc('id_product').value;
  $.ajax({
     url: '/products/check_equiv_destino/',
     data: {
       'id_product': id_product,
       'id_unidad_origen': id_unidad_origen,
     },
     dataType: 'json',
     type: 'GET',
     success: function(data) {
       doc('unidad_destino').value = 0;
       for(var i=0; i<data.unidadesTotal.length; i++){
         doc('optunidest'+data.unidadesTotal[i]).disabled = false;
       }
       for(var i=0; i<data.unidades.length; i++){
         doc('optunidest'+data.unidades[i]).disabled = true;
       }
       doc('unidad_destino').disabled = false;
       doc('optunidest'+doc('optunidest'+id_unidad_origen).value).disabled = true;
     }
  });
}
























//
