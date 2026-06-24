document.addEventListener("DOMContentLoaded", () => {

    const d = window.dashboardData;

    new Chart(
        document.getElementById("graficoEstado"),
        {
            type: "doughnut",

            data: {
                labels: ["Normales", "Anómalos"],

                datasets: [{
                    data: [
                        d.normales,
                        d.anomalos
                    ],

                    backgroundColor: [
                        "#22c55e",
                        "#ef4444"
                    ],

                    borderWidth: 0
                }]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: "65%"
            }
        }
    );

    new Chart(
        document.getElementById("graficoAlertas"),
        {
            type: "bar",

            data: {

                labels: [
                    "Alta",
                    "Media",
                    "Baja"
                ],

                datasets: [{
                    data: [
                        d.alta,
                        d.media,
                        d.baja
                    ],

                    backgroundColor: [
                        "#dc2626",
                        "#f59e0b",
                        "#16a34a"
                    ],

                    borderRadius: 8
                }]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        }
    );

});