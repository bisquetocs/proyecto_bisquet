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

// EXTRA (LITTLE USE BUT NO USELESS)
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

// ADD OR EDIT PRODUCT (INFO AND PRICES)
function editProduct(id_product){
  cancelAgregar();
  //INFO GENERAL DEL PRODUCTO
  document.getElementById('editar_producto').hidden = false;
  document.getElementById('agregar_producto').hidden = true;
  document.getElementById('no_selected').hidden = true;
  document.getElementById('selected').hidden = false;
  //PRECIOS
  document.getElementById('selected_price').hidden = false;
  document.getElementById('no_selected_price').hidden = true;
  document.getElementById('adding_price').hidden = true;
  //EQUIVALENCIAS
  document.getElementById('selected_equiv').hidden = false;
  document.getElementById('no_selected_equiv').hidden = true;
  document.getElementById('adding_equiv').hidden = true;
  //SELECTS AND OTHERS
  document.getElementById('unidad_de_medida').value = 0;
  document.getElementById('price').value = null;
  document.getElementById('cantidad_origen').disabled=true;
  document.getElementById('cantidad_origen').value= 1;
  document.getElementById('unidad_origen').value = 0;
  document.getElementById('unidad_destino').value = 0;
  document.getElementById('unidad_destino').disabled = true;
  document.getElementById('cantidad_destino').value = null;
  var id_product = id_product;
  $.ajax({
     url: '/products/get_product/',
     data: {
        'id_product': id_product
     },
     dataType: 'json',
     type: 'GET',
     success: function(data) {
       document.getElementById('id_product').value = data.id_product;
       document.getElementsByClassName('nombre_producto');
       list = document.getElementsByClassName('nombre_producto');
       for(var i=0; i<list.length; i++){
         list[i].innerHTML = capitalizeFirstLetter(data['nombre']);
       }
       document.getElementById('nombre').value = capitalizeFirstLetter(data['nombre']);
       document.getElementById('descripcion').innerHTML = data.descripcion;
       document.getElementById('codigo').value = data.codigo;
       document.getElementById('activo').checked = data.activo;
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
       document.getElementById('id_product').value = data.id_product;
       document.getElementById('precios_de_producto').innerHTML = '<div class="col-5"><h6>Unidad de medida:</h6></div>'+
                                                    '<div class="col-4"><h6>Precio:</h6></div>'+
                                                    '<div class="col-3"></div>';
       for(var i=0; i<data.id_unidad.length; i++){
         document.getElementById('precios_de_producto').innerHTML = document.getElementById('precios_de_producto').innerHTML +
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
       document.getElementById('equivalencias_de_producto').innerHTML = '<br />'+
                                               '<p style="color:gray">'+
                                                'Aún no registras ninguna equivalencia'+
                                               '</p>'+
                                               '<br /><br />';
       if(data){
         if(data.id_unidad_origen.length!=0){
           document.getElementById('equivalencias_de_producto').innerHTML = '';
           for(var i=0; i<data.id_unidad_origen.length; i++){
             document.getElementById('equivalencias_de_producto').innerHTML = document.getElementById('equivalencias_de_producto').innerHTML+
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
  document.getElementById('selected_price').hidden = true;
  document.getElementById('no_selected_price').hidden = false;
  document.getElementById('adding_price').hidden = true;
  //EQUIVALENCIAS
  document.getElementById('selected_equiv').hidden = true;
  document.getElementById('no_selected_equiv').hidden = false;
  document.getElementById('adding_equiv').hidden = true;
  //INFO GENERAL DEL PRODUCTO
  document.getElementById('editar_producto').hidden = false;
  document.getElementById('selected').hidden = true;
  document.getElementById('no_selected').hidden = false;
  document.getElementById('agregar_producto').hidden = true;
  //OTHERS
  document.getElementById('id_product').value = '';
  document.getElementById('nombre').value = '';
  document.getElementById('descripcion').innerHTML = '';
  document.getElementById('codigo').value = '';
  document.getElementById('cantidad_origen').disabled=true;
  //document.getElementById('activo').checked = True;
  document.getElementById('precios_de_producto').innerHTML = ' ';
  list = document.getElementsByClassName('nombre_producto');
  for(var i=0; i<list.length; i++){
    list[i].innerHTML = '';
  }
}

function showAgregar(){
  cancelEdit();
  document.getElementById('selected_price').hidden = true;
  document.getElementById('no_selected_price').hidden = true;
  document.getElementById('adding_price').hidden = false;

  document.getElementById('selected_equiv').hidden = true;
  document.getElementById('no_selected_equiv').hidden = true;
  document.getElementById('adding_equiv').hidden = false;

  document.getElementById('editar_producto').hidden = true;
  document.getElementById('agregar_producto').hidden = false;
}

function cancelAgregar(){
  //PRICE
  document.getElementById('selected_price').hidden = true;
  document.getElementById('no_selected_price').hidden = false;
  document.getElementById('adding_price').hidden = true;
  //EQUIV
  document.getElementById('selected_equiv').hidden = true;
  document.getElementById('no_selected_equiv').hidden = false;
  document.getElementById('adding_equiv').hidden = true;
  //INFO GENERAL
  document.getElementById('editar_producto').hidden = false;
  document.getElementById('selected').hidden = true;
  document.getElementById('no_selected').hidden = false;
  document.getElementById('agregar_producto').hidden = true;
  //OTHERS
  document.getElementById('nombre').value = '';
  document.getElementById('descripcion').innerHTML = '';
  document.getElementById('codigo').value = '';
}

function ableUnable(id_product){
  document.getElementById('ableUnable'+id_product).innerHTML = '<div style="color:gary">'+
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
         document.getElementById('ableUnable'+id_product).innerHTML = '<div style="color:green" onclick="ableUnable('+id_product+')">'+
                                                                      '<span class="fa fa-eye"></span>'+
                                                                      '</div>';
       }else{
         document.getElementById('ableUnable'+id_product).innerHTML = '<div style="color:red" onclick="ableUnable('+id_product+')">'+
                                                                      '<span class="fa fa-eye-slash"></span>'+
                                                                      '</div>';
       }
     }
  });
}
// PRODCUT PRICES
function checaUnidad(){
  var id_product = document.getElementById('id_product').value;
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
           document.getElementById('optuni'+data.unidadesTotal[i]).disabled = false;
         }
         for(var i=0; i<data.unidades.length; i++){
           document.getElementById('optuni'+data.unidades[i]).disabled = true;
         }
       }
    });
  }
}

function addPrice(){
  var id_product = document.getElementById('id_product').value;
  var id_unidad = document.getElementById('unidad_de_medida').value;
  var cantidad = document.getElementById('price').value;
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
  document.getElementById('pre'+id_price).disabled = false;
  document.getElementById('editThisPrice'+id_price).hidden = true;
  document.getElementById('editThisPriceSection'+id_price).hidden = false;
  document.getElementById('pre'+id_price).name = document.getElementById('pre'+id_price).value;
}

function deleteThisPrice(id_price){
  var producto = document.getElementById('nombre').value;
  var unidad = document.getElementById('uni'+id_price).value;
  var id_product = document.getElementById('id_product').value;
  var id_unidad = document.getElementById('uni'+id_price).name;
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
  var id_product = document.getElementById('id_product').value;
  var id_unidad = document.getElementById('uni'+id_price).name;
  var cantidad = document.getElementById('pre'+id_price).value;
  if (document.getElementById('pre'+id_price).name != cantidad){
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
         document.getElementById('pre'+id_price).disabled = true;
         document.getElementById('editThisPrice'+id_price).hidden = false;
         document.getElementById('editThisPriceSection'+id_price).hidden = true;
         document.getElementById('pre'+id_price).value = cantidad;
         document.getElementById('pre'+id_price).name = cantidad;
       }
    });
  } else{
    cancelPrice(id_price);
  }
}

function cancelPrice(id_price){
  document.getElementById('pre'+id_price).disabled = true;
  document.getElementById('editThisPrice'+id_price).hidden = false;
  document.getElementById('editThisPriceSection'+id_price).hidden = true;
  document.getElementById('pre'+id_price).value = document.getElementById('pre'+id_price).name;
}

// PRODUCT EQUIVALENCIAS
function registrarEquivalencia(){
  var id_product = document.getElementById('id_product').value;
  var id_unidad_origen = document.getElementById('unidad_origen').value;
  var cantidad_origen = document.getElementById('cantidad_origen').value;
  var id_unidad_destino = document.getElementById('unidad_destino').value;
  var cantidad_destino = document.getElementById('cantidad_destino').value;

  if(cantidad_destino > 0 && cantidad_destino != null
        && cantidad_origen > 0 && cantidad_origen != null
        && id_unidad_origen!=0 && id_unidad_origen!=null
        && id_unidad_destino!=0 && id_unidad_destino!=null
        && id_unidad_destino!=id_unidad_origen){
    $.ajax({
       url: '/products/add_equivalencia/',
       data: {
          'id_product': id_product,
          'id_unidad_origen': id_unidad_origen,
          'cantidad_origen': cantidad_origen,
          'id_unidad_destino': id_unidad_destino,
          'cantidad_destino': cantidad_destino,
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
  document.getElementById('equiv'+id_equiv).hidden = false;
}

function hideDeleteEquiv(id_equiv){
  document.getElementById('equiv'+id_equiv).hidden = true;
}

function delete_equiv(id_equiv){
  var id_product = document.getElementById('id_product').value;
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
  var id_product = document.getElementById('id_product').value;
  $.ajax({
     url: '/products/check_equiv_destino/',
     data: {
       'id_product': id_product,
       'id_unidad_origen': id_unidad_origen,
     },
     dataType: 'json',
     type: 'GET',
     success: function(data) {
       document.getElementById('unidad_destino').value = 0;
       for(var i=0; i<data.unidadesTotal.length; i++){
         document.getElementById('optunidest'+data.unidadesTotal[i]).disabled = false;
       }
       for(var i=0; i<data.unidades.length; i++){
         document.getElementById('optunidest'+data.unidades[i]).disabled = true;
       }
       document.getElementById('unidad_destino').disabled = false;
       document.getElementById('optunidest'+document.getElementById('optunidest'+id_unidad_origen).value).disabled = true;
     }
  });
}
























//
