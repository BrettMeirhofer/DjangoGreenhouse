function deltas_to_time(deltas){
    times = []
    deltas.forEach((element => {
                today = new Date()
                today.setHours(today.getHours() - parseInt(element))
                current_time = today.getHours() + ":00"
                times.push(current_time)
            }));
    return times
}

function deltas_to_days(deltas){
    times = []
    deltas.forEach((element => {
        today = new Date()
        today.setDate(today.getDate() - parseInt(element))
        current_time = (today.getMonth()+1) + "/" + today.getDate()
        times.push(current_time)
    }));
    return times

}

function no_parse(deltas){
}


function generate_line_graph(element, url, title, color, y_title, delta_func){
    var mychart = $(element)
	var ctx3 = mychart.get(0)
    var url = $(url).attr("data-url");
	$.ajax({
        url: url,
        success: function (data) {
            var times = delta_func(data.label)
			const myChart = new Chart(ctx3, {
				type: 'line',
				data: {
					labels: times,
					datasets: [{
						data: data.y,
						backgroundColor: color,
						borderColor: color,
						borderWidth: 1
					}]
				},
				options: {
					responsive: false,
					scales: {
						y: {

							beginAtZero: true,
							title: {
								display: true,
								text: y_title
							},
							ticks: {
								beginAtZero: true
							  }


						}

					},
					plugins: {
						title: {
							display: true,
							text: title
						},
						legend: {
							display: false
						}
					}
				}
			});

        }
    })
}

function temp_chart(delta_func){
    generate_line_graph("#chart1", "#temp_series", "Greenhouse Temperature", "rgba(200, 150, 0, 1)", "Temperature (F)", no_parse)
}

function humd_chart(delta_func){
    generate_line_graph("#chart2", "#humd_series", "Greenhouse Humidity", "rgba(0, 200, 0, 1)", "Humidity %", no_parse)
}

function water_chart(delta_func){
    generate_line_graph("#chart3", "#water_series", "Greenhouse Water Level", "rgba(0, 0, 200, 1)", "Fill %", no_parse)
}

function heater_chart(delta_func){
    generate_line_graph("#chart4", "#heater_series", "Greenhouse Heater Uptime", "rgba(200, 0, 0, 1)", "Uptime %", no_parse)
}