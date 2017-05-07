var updateInterval = 1000;
var player = dashjs.MediaPlayer().create();
player.getDebug().setLogToBrowserConsole(false);
var metricsInterval = null;

player.on(dashjs.MediaPlayer.events.STREAM_INITIALIZED, function(e){
	console.log(e.type);
	clearInterval(metricsInterval);
	metricsInterval = setInterval(function(){
		updateMetrics("video");
		updateMetrics("audio");
	}, updateInterval);

});

function updateMetrics(type){
	var metrics = player.getMetricsFor(type);
	var dashMetrics = player.getDashMetrics();
	if (metrics && dashMetrics){
		var bufferLevel = dashMetrics.getCurrentBufferLevel(metrics);
		$("#buffer").text("Buffer length: " + bufferLevel);
	}
};


