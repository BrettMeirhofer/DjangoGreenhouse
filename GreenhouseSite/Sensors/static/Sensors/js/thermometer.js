                     <html>
<head>
  <script src="https://cdn.anychart.com/releases/v8/js/anychart-base.min.js"></script>
  <script src="https://cdn.anychart.com/releases/v8/js/anychart-ui.min.js"></script>
  <script src="https://cdn.anychart.com/releases/v8/js/anychart-exports.min.js"></script>
  <script src="https://cdn.anychart.com/releases/v8/js/anychart-linear-gauge.min.js"></script>
  <link href="https://cdn.anychart.com/releases/v8/css/anychart-ui.min.css" type="text/css" rel="stylesheet">
  <link href="https://cdn.anychart.com/releases/v8/fonts/css/anychart-font.min.css" type="text/css" rel="stylesheet">
  <style type="text/css">

    html,
    body,
    #container {
      width: 100%;
      height: 100%;
      margin: 0;
      padding: 0;
    }

</style>
</head>
<body>

  <div id="container"></div>


  <script>

    anychart.onDocumentReady(function () {
      drawLinearGauge(28)
      drawLinearGauge(22)


      // Helper function to create linear gauge
      function drawLinearGauge(value) {
        var gauge = anychart.gauges.linear();
        gauge.data([value]);
        gauge.tooltip(false);

        // Create thermometer title
        gauge
          .title()
          .enabled(true)
          .text(value + '°')
          .fontColor('#212121')
          .fontWeight(600)
          .fontSize(24)
          .orientation('bottom')
          .useHtml(true)
          .padding([10, 0, 5, 0]);

        // Create thermometer pointer
        var thermometer = gauge.thermometer(0);

        // Set thermometer settings
        thermometer.offset('1').width('3%').fill('#64b5f6').stroke('#64b5f6');

        // Set scale settings
        var scale = gauge.scale();
        scale
          .minimum(0)
          .maximum(40)
          .ticks({ interval: 10 })
          .minorTicks({ interval: 1 });
        // Set axis and axis settings
        var axis = gauge.axis();
        axis.scale(scale).minorTicks(true).width('0').offset('0%');

        // Set text formatter for axis labels
        axis.labels().useHtml(true).format('{%Value}°');

        return gauge;
      }


    });

</script>
</body>
</html>
