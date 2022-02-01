$(document).ready(function () {
    temp_chart(deltas_to_days)
    humd_chart(deltas_to_days)
    water_chart(deltas_to_days)
    heater_chart(deltas_to_days)

    var x = window.matchMedia("(min-width: 1200px)")
    if (x.matches) {
        $(".canvas_graph").css("display", "inline-block")
    }
})