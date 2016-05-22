c3.generate({
    bindto: "#time-chart",
    data: {
        x: 'x',
        xFormat: '%Y-%m-%d %H:%M:%S',
        colors: {
            "connect": "#3498DB",
            "disconnect": "#E74C3C"
        },
        columns: [
            connection_log.x,
            connection_log.connect,
            connection_log.disconnect
        ]
    },
    axis: {
        x: {
            type: 'timeseries',
            tick: {
                format: '%Y-%m-%d %H:%M:%S'
            }
        }
    }
});
