document.addEventListener("DOMContentLoaded", () => {

    Chart.register(ChartDataLabels);

    const datos = window.reportesData;

    const graficoEstado =
        document.getElementById("graficoEstado");

    if (graficoEstado) {

        new Chart(graficoEstado, {

            type: "doughnut",

            data: {

                labels: [
                    "Normales",
                    "Anómalos"
                ],

                datasets: [{

                    data: [
                        datos.total_normales,
                        datos.total_anomalias
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
                cutout: '65%',
                plugins: {
                    legend: {
                        position: 'bottom'
                    },

                    tooltip: {
                        enabled: true
                    }
                }
            }

        });

    }

    const graficoPrioridad =
        document.getElementById("graficoPrioridad");

    if (graficoPrioridad) {

        new Chart(graficoPrioridad, {

            type: "bar",

            data: {

                labels: [
                    "Alta",
                    "Media",
                    "Baja"
                ],

                datasets: [{

                    data: [
                        datos.alertas_alta,
                        datos.alertas_media,
                        datos.alertas_baja
                    ],

                    backgroundColor: [
                        "#dc3545",
                        "#ffc107",
                        "#198754"
                    ],

                    borderRadius: 8,
                    maxBarThickness: 70

                }]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },

                    datalabels: {
                        anchor: 'end',
                        align: 'top',
                        color: '#111827',
                        font: {
                            weight: 'bold'
                        }
                    }
                },

                scales: {

                    y: {

                        beginAtZero: true,

                        ticks: {
                            precision: 0
                        }

                    }

                }

            }

        });

    }

});