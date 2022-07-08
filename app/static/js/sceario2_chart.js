google.charts.load('current', { 'packages': ['corechart'] });
google.charts.setOnLoadCallback(drawVisualization);

function drawVisualization() {
    arrayToData = scenario_2_data.map(pj => [`${summary_type} ${pj.date}`, parseFloat(pj.closing_balance / 1000000), parseFloat(pj.subtotal_revenues / 1000000), parseFloat(pj.subtotal_spending / 1000000)])
    arrayToData.unshift(['Year', 'Closing balance', 'Revenues', 'Spending'])

    // Some raw data (not necessarily accurate)
    var data = google.visualization.arrayToDataTable(arrayToData);

    var options = {
        title: `FMLI Program - Projected Fiscal Activity (${summary_type}) - ${scenario_2}`,
        animation: { startup: true },
        legend: {
            alignment: 'center',
            position: "bottom",
        },
        // selectionMode: 'multiple',
        pointSize: 4,
        vAxis: {
            title: 'Dollars in millions',
            format: 'currency',
            viewWindowMode: 'explicit',
            viewWindow: {
                max: 700,
                min: 0
            }
        },
        hAxis: {
            title: 'Calendar years',
        },
        seriesType: 'bars',
        series: {
            0: {
                color: "#a7a7ff"
            },
            1: { type: 'line' },
            2: { type: 'line' }
        }
    };

    var chart = new google.visualization.ComboChart(document.getElementById('chart_div_v2'));
    chart.draw(data, options);
}