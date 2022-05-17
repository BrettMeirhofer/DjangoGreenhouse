$(document).ready(function () {
    temp_chart(get_days_string)
    humd_chart(get_days_string)
    water_chart(get_days_string)
    heater_chart(get_days_string)

    var x = window.matchMedia("(min-width: 1200px)")
    if (x.matches) {
        $(".canvas_graph").css("display", "inline-block")
    }
})