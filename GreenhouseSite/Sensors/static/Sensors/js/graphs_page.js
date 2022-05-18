$(document).ready(function () {
    temp_chart("d")
    humd_chart("d")
    water_chart("d")
    heater_chart("d")

    var x = window.matchMedia("(min-width: 1200px)")
    if (x.matches) {
        $(".canvas_graph").css("display", "inline-block")
    }
})