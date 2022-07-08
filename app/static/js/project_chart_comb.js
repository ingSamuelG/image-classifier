google.charts.load('current', { 'packages': ['corechart'] });
google.charts.setOnLoadCallback(drawVisualization);

function drawVisualization() {
    let to_float = chart_values.map((array_of_v) => {
        return array_of_v.map((value, index) => {
            if (index != 0)
                return (value / 1000000)
            else
                return value.toString()
        })
    })

    to_float.unshift(['Year', `Closing balance-${scenario_1}`, `Closing balance-${scenario_2}`, `Revenues-${scenario_1}`, `Revenues-${scenario_2}`, `Spending-${scenario_1}`, `Spending-${scenario_2}`])

    // Some raw data (not necessarily accurate)
    var data = google.visualization.arrayToDataTable(to_float);

    var options = {
        title: `FMLI Program - Projected Fiscal Activity comparison (${summary_type}): ${scenario_1} - ${scenario_2}`,
        animation: { startup: true },
        // legend: {
        //     alignment: 'center',
        //     position: "bottom",
        // },
        // selectionMode: 'multiple',
        pointSize: 4,
        vAxis: {
            title: 'Dollars in millions',
            format: 'currency'
        },
        hAxis: {
            title: 'Calendar years',
        },
        seriesType: 'bars',
        series: {
            0: {
                color: "#aca7d0"
            },
            1: {
                color: "#a7a7ff"
            },
            2: { type: 'line', color: "3c3096" },
            3: { type: 'line', color: "4a6c6f" },
            4: { type: 'line' },
            5: { type: 'line' },
        }
    };

    var chart = new google.visualization.ComboChart(document.getElementById('chart_div_v1'));
    chart.draw(data, options);
}