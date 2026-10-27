function renderCharts(metricsData) {
    if (!metricsData || metricsData.length === 0) return;

    const labels = metricsData.map((_, index) => `Test ${index + 1}`);
    const complexity = metricsData.map(m => m.complexity);
    const efficiency = metricsData.map(m => m.efficiency);
    const readability = metricsData.map(m => m.readability);

    // Line Chart
    const ctxLine = document.getElementById('lineChart').getContext('2d');
    new Chart(ctxLine, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Complexity',
                    data: complexity,
                    borderColor: '#4e73df',
                    fill: false
                },
                {
                    label: 'Efficiency',
                    data: efficiency,
                    borderColor: '#1cc88a',
                    fill: false
                },
                {
                    label: 'Readability',
                    data: readability,
                    borderColor: '#36b9cc',
                    fill: false
                }
            ]
        },
        options: {
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 10
                }
            }
        }
    });

    // Bar Chart
    const ctxBar = document.getElementById('barChart').getContext('2d');
    const avgComplexity = complexity.reduce((a, b) => a + b, 0) / complexity.length;
    const avgEfficiency = efficiency.reduce((a, b) => a + b, 0) / efficiency.length;
    const avgReadability = readability.reduce((a, b) => a + b, 0) / readability.length;

    new Chart(ctxBar, {
        type: 'bar',
        data: {
            labels: ['Avg Complexity', 'Avg Efficiency', 'Avg Readability'],
            datasets: [{
                label: 'Average Metrics',
                data: [avgComplexity, avgEfficiency, avgReadability],
                backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc']
            }]
        },
        options: {
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 10
                }
            }
        }
    });
}
