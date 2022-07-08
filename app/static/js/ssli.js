google.charts.load('current', { 'packages': ['corechart'] });
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
    // arrayToData = [historicals.map((hs) => { [hs.date, hs.change * 100] })]
    arrayToData = historicals.map(hs => [String(hs.date), parseFloat(hs.percent_change * 100)])
    arrayToData.unshift(["Year", "Percentage change"])
    var data = google.visualization.arrayToDataTable(arrayToData);

    var options = {
        title: `Taxable Wage Base - % Annual Change  ${historicals[0].date} - ${historicals[historicals.length - 1].date} (Based on the Social Security Integration Level)`,
        // curveType: 'function',
        series: {
            0: { color: "#6a5cce" }
        },
        vAxis: {
            format: '#\'%\''
        },
        legend: { position: 'bottom' }
    };

    var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

    chart.draw(data, options);
}