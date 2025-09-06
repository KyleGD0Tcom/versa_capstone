document.addEventListener('DOMContentLoaded', function () {
  const toggleSidebarBtn = document.getElementById('toggleSidebar');
  const sidebar = document.getElementById('sidebar');
  const mainContent = document.getElementById('mainContent'); // To track clicks outside the sidebar

  // Toggle sidebar when hamburger icon is clicked
  toggleSidebarBtn.addEventListener('click', function () {
    sidebar.classList.toggle('show'); // Toggle 'show' class to show/hide the sidebar
  });

  // Close sidebar when clicking outside of the sidebar
  document.addEventListener('click', function (e) {
    // Check if the click is outside the sidebar or hamburger menu
    if (!sidebar.contains(e.target) && !toggleSidebarBtn.contains(e.target)) {
      sidebar.classList.remove('show'); // Remove the 'show' class to close the sidebar
    }
  });

  // Prevent closing the sidebar if the user clicks inside the sidebar or on the toggle button
  sidebar.addEventListener('click', function (e) {
    e.stopPropagation(); // Prevent event from bubbling up to the document listener
  });
});


//SALES FORECAST JS

// document.addEventListener("DOMContentLoaded", function () {
//     const ctx = document.getElementById("saleForecastChart").getContext("2d");
//     new Chart(ctx, {
//       type: "bar",
//       data: {
//         labels: ["21", "22", "23", "24", "25", "26", "27", "28"],
//         datasets: [
//           {
//             label: "Forecast Sale",
//             data: [25000, 40000, 22000, 52000, 38000, 27000, 30000, 24000],
//             backgroundColor: "#6ce5e8",
//             barPercentage: 1,
//             categoryPercentage: 0.5,
//           },
//           {
//             label: "Actual Sale",
//             data: [40000, 35000, 33000, 42000, 36000, 44000, 41000, 35000],
//             backgroundColor: "#2d8bba",
//             barPercentage: 1,
//             categoryPercentage: 0.5,
//           },
//         ],
//       },
//       options: {
//         responsive: true,
//         maintainAspectRatio: false,
//         plugins: {
//           legend: {
//             position: "top",
//             labels: {
//               usePointStyle: true,
//               pointStyle: "circle",
//               font: {
//                 size: 12,
//               },
//               color: "#333",
//             },
//           },
//         },
//         scales: {
//           x: {
//             title: {
//               display: true,
//               text: "Day",
//               color: "#999",
//               font: { style: "italic" },
//             },
//             ticks: {
//               color: "#333",
//             },
//             grid: {
//               display: false,
//             },
//           },
//           y: {
//             beginAtZero: true,
//             title: {
//               display: true,
//               text: "Amount",
//               color: "#999",
//               font: { style: "italic" },
//             },
//             ticks: {
//               callback: (value) => `${value / 1000}k`,
//               color: "#333",
//             },
//             grid: {
//               color: "#ddd",
//               borderDash: [4, 4],
//             },
//           },
//         },
//       },
//     });
//   });


// saleForecastChartAdminDashboard

document.addEventListener("DOMContentLoaded", function () {
  const ctx = document.getElementById("saleForecastChartAdminDashboard").getContext("2d");
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["24", "22", "23", "24", "25", "26", "27", "28"],
      datasets: [
        {
          label: "Forecast Sale",
          data: [25000, 40000, 22000, 52000, 38000, 27000, 30000, 24000],
          backgroundColor: "#6ce5e8",
          barPercentage: 1,
          categoryPercentage: 0.5,
        },
        {
          label: "Actual Sale",
          data: [40000, 35000, 33000, 42000, 36000, 44000, 41000, 35000],
          backgroundColor: "#2d8bba",
          barPercentage: 1,
          categoryPercentage: 0.5,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "top",
          labels: {
            usePointStyle: true,
            pointStyle: "circle",
            font: {
              size: 12,
            },
            color: "#333",
          },
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: "Day",
            color: "#999",
            font: { style: "italic" },
          },
          ticks: {
            color: "#333",
          },
          grid: {
            display: false,
          },
        },
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "Amount",
            color: "#999",
            font: { style: "italic" },
          },
          ticks: {
            callback: (value) => `${value / 1000}k`,
            color: "#333",
          },
          grid: {
            color: "#ddd",
            borderDash: [4, 4],
          },
        },
      },
    },
  });
});
