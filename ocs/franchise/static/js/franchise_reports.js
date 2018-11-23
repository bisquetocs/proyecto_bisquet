var lineChart = document.getElementById("dateorder");
var doughnutChart = document.getElementById("percentage_order");

var doughnutChart3 = document.getElementById("percentage_cost");
doughnutChart.height = 100;

doughnutChart3.height = 100;


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
            labels: data.provider_names,
            datasets: [
              {
                label: "$:",
                backgroundColor: data.provider_color,
                data: data.total_inversion
              }
            ]
          },
          options: {
            title: {
              display: true,
            },
            legend: {
              display: false
            }
          }
      });



    },
    error: function(error_data){
      alert("Ocurrió un error desplegando el dashboard, inténtalo de nuevo más tarde");
    }
})
