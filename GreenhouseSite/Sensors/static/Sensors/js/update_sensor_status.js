$(document).ready(function () {

    var url = $("#sensor_data").attr("data-url");
    $.ajax({
        url: url,
        success: function (data) {
            fah_temp = ((parseFloat(data.readings[0]) * 9/5) + 32).toFixed(2)
            temp_string = fah_temp + "F / " + data.readings[0] + "C"
            $("#temp").text(temp_string)
            $("#humd").text(data.readings[1] + "%")
            water_text = $("#water")
            water_text.text(data.readings[2] + "%")
            if (data.readings[2] < 40){
                $("#water").css("color", "red");
            }
            else if (data.readings[2] < 60){
                $("#water").css("color", "yellow");
            }
            else{
                $("#water").css("color", "green");
            }
            if (data.heater){
                heater_status = "ON"
            }
            else{
                heater_status = "OFF"
            }
            $("#heater").text(heater_status)

        }
    })


    var mychart = $('#chart1')
	var ctx1 = mychart.get(0)
    var url = $("#temp_series").attr("data-url");
	$.ajax({
        url: url,
        success: function (data) {
            var times = deltas_to_time(data.label)
			const myChart = new Chart(ctx1, {
				type: 'line',
				data: {
					labels: times,
					datasets: [{
						data: data.y,
						backgroundColor: 'rgba(200, 150, 0, 1)',
						borderColor: 'rgba(200, 100, 0, 1)',
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
								text: "Temperature (F)"
							},
							ticks: {
								beginAtZero: true
							  }


						}

					},
					plugins: {
						title: {
							display: true,
							text: "Greenhouse Temperature"
						},
						legend: {
							display: false
						}
					}
				}
			});

        }
    })

    var mychart = $('#chart2')
	var ctx2 = mychart.get(0)
    var url = $("#humd_series").attr("data-url");
	$.ajax({
        url: url,
        success: function (data) {
            var times = deltas_to_time(data.label)
			const myChart = new Chart(ctx2, {
				type: 'line',
				data: {
					labels: times,
					datasets: [{
						data: data.y,
						backgroundColor: 'rgba(0, 200, 0, 1)',
						borderColor: 'rgba(0, 200, 0, 1)',
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
								text: "Humidity %"
							},
							ticks: {
								beginAtZero: true
							  }


						}

					},
					plugins: {
						title: {
							display: true,
							text: "Greenhouse Humidity"
						},
						legend: {
							display: false
						}
					}
				}
			});

        }
    })

    var mychart = $('#chart3')
	var ctx3 = mychart.get(0)
    var url = $("#water_series").attr("data-url");
	$.ajax({
        url: url,
        success: function (data) {
            var times = deltas_to_time(data.label)
			const myChart = new Chart(ctx3, {
				type: 'line',
				data: {
					labels: times,
					datasets: [{
						data: data.y,
						backgroundColor: 'rgba(0, 0, 200, 1)',
						borderColor: 'rgba(0, 0, 200, 1)',
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
								text: "Fill %"
							},
							ticks: {
								beginAtZero: true
							  }


						}

					},
					plugins: {
						title: {
							display: true,
							text: "Greenhouse Water Level"
						},
						legend: {
							display: false
						}
					}
				}
			});

        }
    })

    var mychart = $('#chart4')
	var ctx4 = mychart.get(0)
    var url = $("#heater_series").attr("data-url");
	$.ajax({
        url: url,
        success: function (data) {
            var times = deltas_to_time(data.label)
			const myChart = new Chart(ctx4, {
				type: 'line',
				data: {
					labels: times,
					datasets: [{
						data: data.y,
						backgroundColor: 'rgba(200, 0, 0, 1)',
						borderColor: 'rgba(200, 0, 0, 1)',
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
								text: "Uptime %"
							},
							ticks: {
								beginAtZero: true
							  }


						}

					},
					plugins: {
						title: {
							display: true,
							text: "Heater Uptime"
						},
						legend: {
							display: false
						}
					}
				}
			});

        }
    })
})

function deltas_to_time(deltas){
    times = []
    deltas.forEach((element => {
                today = new Date()
                today.setSeconds(today.getSeconds() - parseInt(element))
                current_time = today.getHours() + ":" + String(today.getMinutes()).padStart(2, "0")
                times.push(current_time)
            }));
    return times
}

