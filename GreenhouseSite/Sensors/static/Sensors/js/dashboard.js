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
            water_percent = data.readings[2]
            $("#air_tank").css("height", 100 - data.readings[2])
            $("#water_tank").css("height", data.readings[2] - 5)
            $("#Soil1").text(data.readings[3])
            $("#Soil2").text(data.readings[4])
            $("#Soil3").text(data.readings[5])
            if (data.heater){
                heater_status = "ON"
                $("#heater_on").css("visibility", "visible")
                $("#heater_off").css("visibility", "hidden")
            }
            else{
                heater_status = "OFF"
                $("#heater_on").css("visibility", "hidden")
                $("#heater_off").css("visibility", "visible")
            }
            $("#heater_tooltip").text("Heater: " + heater_status)

        }
    })

    generate_line_graph("#chart1", "#temp_series", "Greenhouse Temperature", "rgba(200, 150, 0, 1)", "Temperature (F)")
    generate_line_graph("#chart2", "#humd_series", "Greenhouse Humidity", "rgba(0, 200, 0, 1)", "Humidity %")
    generate_line_graph("#chart3", "#water_series", "Greenhouse Water Level", "rgba(0, 0, 200, 1)", "Fill %")
    generate_line_graph("#chart4", "#heater_series", "Greenhouse Heater Uptime", "rgba(200, 0, 0, 1)", "Uptime %")

    var x = window.matchMedia("(min-width: 1200px)")
    if (x.matches) {
        $(".canvas_graph").css("display", "inline-block")
    }
})