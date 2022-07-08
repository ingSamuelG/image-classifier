google.charts.load('current', { 'packages': ['corechart'] });
google.charts.setOnLoadCallback(drawVisualization);

function drawVisualization() {
    arrayToData = scenario_1_data.map(pj => [`${summary_type} ${pj.date}`, parseFloat(pj.closing_balance / 1000000), parseFloat(pj.subtotal_revenues / 1000000), parseFloat(pj.subtotal_spending / 1000000)])
    arrayToData.unshift(['Year', 'Closing balance', 'Revenues', 'Spending'])

    // Some raw data (not necessarily accurate)
    var data = google.visualization.arrayToDataTable(arrayToData);

    var options = {
        title: `FMLI Program - Projected Fiscal Activity (${summary_type}) - ${scenario_1}`,
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
                color: "#aca7d0"
            },
            1: { type: 'line', color: "black" },
            2: { type: 'line', color: "#4a6c6f" }
        }
    };

    var chart = new google.visualization.ComboChart(document.getElementById('chart_div_v1'));
    chart.draw(data, options);
}