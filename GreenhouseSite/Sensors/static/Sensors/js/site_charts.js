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


function generate_line_graph(element, url, title, color, y_title){
    var mychart = $(element)
	var ctx3 = mychart.get(0)
    var url = $(url).attr("data-url");
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