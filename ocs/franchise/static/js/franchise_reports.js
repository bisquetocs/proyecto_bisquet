var lineChart = document.getElementById("dateorder");
var doughnutChart = document.getElementById("percentage_order");
var doughnutChart2 = document.getElementById("percentage_product");
var doughnutChart3 = document.getElementById("percentage_cost");
doughnutChart.height = 200;
doughnutChart2.height = 200;
doughnutChart3.height = 200;


//AJAX Request
/*
$.ajax({
        url: '/franchise/home/ajax_reports',
        data: {
          'username': data
        },
        dataType: 'json',
        success: function (data) {
          alert('WOOO, AJAX!');
        }
      });

*/
// # of orders by date
new Chart(lineChart, {
  type: 'line',
  data: {
    labels: ["","Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo",""],
    datasets: [{
        data: [0,1,5,0,2,3,1,2,0],
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
    }
  }
});

// Percentage of orders from providers
new Chart(doughnutChart, {
    type: 'doughnut',
    data: {
      labels: [
        "Frutas y Verduras Alberto",
        "Carnes Dante",
        "Abarrotes Fátima"
        ],
      datasets: [
        {
          backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f"],
          data: [50,20,30]
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Proveedores favoritos'
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
          backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
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
          backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
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
