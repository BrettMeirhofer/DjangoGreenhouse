function get_hours_string(deltas){
    times = []
    deltas.forEach((element => {
        current_time = new Date(element)
        current_time = current_time.getHours() + ":00"
        times.push(current_time)
    }));
    return times
}

function get_days_string(deltas){
    times = []
    deltas.forEach((element => {
        current_time = new Date(element)
        current_time = (current_time.getMonth()+1) + "/" + current_time.getDate()
        times.push(current_time)
    }));
    return times
}

function get_months_string(deltas){
    times = []
    deltas.forEach((element => {
        current_time = new Date(element)
        current_time = (current_time.getMonth()+1)
        times.push(current_time)
    }));
    return times
}


function generate_line_graph(element, url, title, color, y_title, increment){
    var mychart = $(element)
	var ctx3 = mychart.get(0)
    var url = $(url).attr("data-url");
    var delta_func = ""
    if (increment == "h"){
        delta_func = get_hours_string
    } else if (increment == "d"){
        delta_func = get_days_string
    }
    else if (increment == "m"){
        delta_func = get_months_string
    }
	$.ajax({
        url: url+"?increment="+increment,
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

function temp_chart(increment){
    generate_line_graph("#chart1", "#temp_series", "Greenhouse Temperature", "rgba(200, 150, 0, 1)", "Temperature (F)", increment)
}

function humd_chart(increment){
    generate_line_graph("#chart2", "#humd_series", "Greenhouse Humidity", "rgba(0, 200, 0, 1)", "Humidity %", increment)
}

function water_chart(increment){
    generate_line_graph("#chart3", "#water_series", "Greenhouse Water Level", "rgba(0, 0, 200, 1)", "Fill %", increment)
}

function heater_chart(increment){
    generate_line_graph("#chart4", "#heater_series", "Greenhouse Heater Uptime", "rgba(200, 0, 0, 1)", "Uptime %", increment)
}