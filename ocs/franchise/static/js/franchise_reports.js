var lineChart = document.getElementById("dateorder");
var doughnutChart = document.getElementById("percentage_order");
var doughnutChart2 = document.getElementById("percentage_product");
var doughnutChart3 = document.getElementById("percentage_cost");
doughnutChart.height = 200;
doughnutChart2.height = 200;
doughnutChart3.height = 200;


//AJAX Request


var endpoint = "/franchise/home/ajax_reports/"
var data_requested
$.ajax({
    mehotd: "GET",
    url: endpoint,
    success: function(data){
      console.log(data);
      // # of orders by date
      new Chart(lineChart, {
        type: 'line',
        data: {
          labels: data.days,
          datasets: [{
              data: data.orders_by_day,
              label: "Pedidos",
              borderColor: "#3e95cd",
              fill: true
            }
          ]
        },
        options: {
          title: {
            display: true,
            text: 'Pedidos realizados durante esta semana'
          },
          legend: {
            display: false
          }
        }
      });

      // Percentage of orders from providers
      new Chart(doughnutChart, {
          type: 'doughnut',
          data: {
            labels: data.provider_names,
            datasets: [
              {
                backgroundColor: data.provider_color,
                data: data.provider_num_orders,
              }
            ]
          },
          options: {
            title: {
              display: true,
              text: '# de pedidos por proveedor'
            },
            legend: {
              display: false
            }
          }
      });

      // Percentage of products ordered
      new Chart(doughnutChart2, {
          type: 'doughnut',
          data: {
            labels: [
              "Jitomate",
              "Chile pasilla",
              "Bistec",
              "Leche deslactosada",
              "Azúcar Morena"
              ],
            datasets: [
              {
                label: "Population (millions)",
                backgroundColor: ["#F39C12", "#011F45","#FF4040","#34A853","#4285F4"],
                data: [2478,5267,734,784,433]
              }
            ]
          },
          options: {
            title: {
              display: true,
              text: 'Productos favoritos'
            },
            legend: {
              display: false
            }
          }

      });

      // Percentage of favorite provider
      new Chart(doughnutChart3, {
          type: 'doughnut',
          data: {
            labels: [
              "Frutas y Verduras Alberto",
              "Carnes Dante",
              "Abarrotes Fátima"
              ],
            datasets: [
              {
                label: "Population (millions)",
                backgroundColor: ["#F39C12", "#011F45","#FF4040","#34A853","#4285F4"],
                data: [2478,5267,734]
              }
            ]
          },
          options: {
            title: {
              display: true,
              text: 'Proveedores con mayor inversión'
            },
            legend: {
              display: false
            }
          }
      });



    },
    error: function(error_data){
      alert("Ocurrió un error, inténtalo de nuevo más tarde");
    }
})
