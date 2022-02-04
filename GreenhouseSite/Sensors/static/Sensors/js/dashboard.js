$(document).ready(function () {

    var url = $("#sensor_data").attr("data-url");
    $.ajax({
        url: url,
        success: function (data) {
            fah_temp = ((parseFloat(data.readings[0]) * 9/5) + 32).toFixed(2)
            temp_string = fah_temp + "F / " + data.readings[0] + "C"
            $("#temp").text(temp_string)
            $("#humd").text(data.readings[1] + "%")

            fah_temp = ((parseFloat(data.readings[2]) * 9/5) + 32).toFixed(2)
            temp_string = fah_temp + "F / " + data.readings[2] + "C"
            $("#temp_out").text(temp_string)
            $("#humd_out").text(data.readings[3] + "%")

            water_text = $("#water")
            water_text.text(data.readings[4] + "%")
            water_percent = data.readings[4]
            $("#air_tank").css("height", 100 - data.readings[4])
            $("#water_tank").css("height", data.readings[4] - 5)
            $("#Soil1").text(data.readings[5])
            $("#Soil2").text(data.readings[6])
            $("#Soil3").text(data.readings[7])
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
    temp_chart(deltas_to_time)
    humd_chart(deltas_to_time)
    water_chart(deltas_to_time)
    heater_chart(deltas_to_time)

    var x = window.matchMedia("(min-width: 1200px)")
    if (x.matches) {
        $(".canvas_graph").css("display", "inline-block")
    }
})