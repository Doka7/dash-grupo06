var updateInterval = 1000;
var player = dashjs.MediaPlayer().create();
var url = "/clip_monza_manifest.mpd";
video = document.querySelector("#dash-video-player");
player.initialize(video, url, false);

var metricsInterval = null;

//Metrics
var videoBufferLevel=0;

player.on(dashjs.MediaPlayer.events.STREAM_INITIALIZED, function(e){
	console.log("Event: "+e.type);
	clearInterval(metricsInterval);
	metricsInterval = setInterval(function(){
		updateMetrics("video");
		updateMetrics("audio");
	}, updateInterval);

});

player.on(dashjs.MediaPlayer.events.PLAYBACK_ENDED, function(e){
	console.log("Event: "+e.type);
	clearInterval(metricsInterval);

});

function updateMetrics(type){
	var metrics = player.getMetricsFor(type);
	var dashMetrics = player.getDashMetrics();
	if (metrics && dashMetrics){
		videoBufferLevel = dashMetrics.getCurrentBufferLevel(metrics);
		$("#buffer").text("Buffer length: " + videoBufferLevel);
		//console.log("Video buffer level: " +videoBufferLevel);
	}
};

