var updateInterval = 1000;
var player = dashjs.MediaPlayer().create();
var url = "/clip_monza_manifest.mpd";
video = document.querySelector("#dash-video-player");
player.initialize(video, url, false);

var metricsInterval = null;
var streamInfo=null;
//Metrics
var videoBufferLevel=0;
var droppedFPS=0;
var bitrate=0;

player.on(dashjs.MediaPlayer.events.PLAYBACK_STARTED, function(e){
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

player.on(dashjs.MediaPlayer.events.PLAYBACK_PAUSED, function(e){
	console.log("Event: "+e.type);
	clearInterval(metricsInterval);

});

player.on(dashjs.MediaPlayer.events.PERIOD_SWITCH_COMPLETED, function (e) {
     console.log("Event: "+e.type);
     streamInfo = e.toStreamInfo;
    });

function updateMetrics(type){
	var metrics = player.getMetricsFor(type);
	var dashMetrics = player.getDashMetrics();
	if (metrics && dashMetrics && streamInfo){
		var periodIdx = streamInfo.index;
		var repSwitch = dashMetrics.getCurrentRepresentationSwitch(metrics);
		videoBufferLevel = dashMetrics.getCurrentBufferLevel(metrics);
		droppedFPS = dashMetrics.getCurrentDroppedFrames(metrics) ? dashMetrics.getCurrentDroppedFrames(metrics).droppedFrames : 0;
		bitrate = Math.round(dashMetrics.getBandwidthForRepresentation(repSwitch.to, periodIdx) / 1000);
		$("#"+type+"Buffer").text("Buffer length: " + videoBufferLevel);
		$("#"+type+"fps").text("Dropped Frames: " + droppedFPS);
		$("#"+type+"Bitrate").text("Bitrate: " + bitrate + " kbps");
		//console.log("Video buffer level: " +videoBufferLevel);
	}
};

