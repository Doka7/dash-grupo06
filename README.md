PASOS SEGUIDOS PARA INSTALACIÓN DE SERVIDOR/CLIENTE DASH: 
https://developer.mozilla.org/en-US/docs/Web/HTML/DASH_Adaptive_Streaming_for_HTML_5_Video

1. INSTALACIÓN DE HERRAMIENTAS NECESARIAS

1.1 FFMPEG

	Descarga de FFmpeg para la codificación de audio/vídeo en distintos formatos de calidad que se almacenarán en el servidor. Descarga desde http://www.ffmpeg.org

	Para instalar seguir los pasos indicados en: https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu

	Ejemplos de uso: 
		-audio: $ ffmpeg -i clip_monza.mp4 -acodec libopus -vn -ar 48k audio_48k.webm
		-video: $ ffmpeg -i clip_monza.mp4 -c:v libvpx -f webm -dash 1 -an -s 160x90 -b:v 250k video_160x90_250k.webm

	Para ver las caracteristicas de un codificador en concreto: 

	$ ffmpeg -h encoder=libopus
	...
	Encoder libopus [libopus Opus]:
	    Threading capabilities: no
	    Supported sample rates: 48000 24000 16000 12000 8000
	    Supported sample formats: s16 flt
	    Supported channel layouts: mono stereo 3.0 quad 5.0 5.1 6.1 7.1



1.2 SAMPLEMUXER

	Instalar libwebm, concretamente para instalar la herramienta samplemuxer para agrupar en clusters las distintas calidades de los archivos multimedia. 

	Para instalar: 
		- git clone https://chromium.googlesource.com/webm/libwebm
		- renombrar el Makefile.unix a Makefile y ejecutar 'make'

	Ejemplo de uso: 
	./mkvmuxer_sample -i /home/doka/Escritorio/video_1280x720_1500k.webm -o /var/www/html/video_1280x720_1500k_final.webm
	./mkvmuxer_sample -i /home/doka/Escritorio/audio_48k.webm -o /var/www/html/audio_48k_final.webm -output_cues 1 -cues_on_audio_track 1 -max_cluster_duration 2 -audio_track_number 0



1.3 WEB_DASH_MANIFEST

	Instalar webm-tools, concretamente para instalar la herramienta 'webm_dash_manifest' para crear archivos .mpd 

	Para instalar: 
		- git clone https://github.com/webmproject/webm-tools.git
		- buscar el path de la herramienta que queremos instalar hasta encontrar el Makefile y ejecutar comando 'make'. 

	Ejemplo de uso: 
		./webm_dash_manifest -o /var/www/html/my_video_manifest.mpd \
	  	-as id=0,lang=eng \
	  	-r id=1,file=/var/www/html/video_1280x720_1500k_final.webm \
	  	-r id=2,file=/var/www/html/video_640x360_750k_final.webm \
	  	-r id=3,file=/var/www/html/video_320x180_500k_final.webm \
	  	-r id=4,file=/var/www/html/video_160x90_250k_final.webm \
	  	-as id=1,lang=eng \
	  	-r id=5,file=/var/www/html/audio_48k_final.webm

	Importante que los vídeos usen codec VP8, para VP9 todavía no hay soporte. 
	Para comprobar si un archivo MPD es correcto, existen validators como: http://www-itec.uni-klu.ac.at/dash/?page_id=605


2. ALMACENAMIENTO DE ARCHIVOS MULTIMEDIA EN EL SERVIDOR

Una vez tenemos todo instalado, hay que alojar en un servidor web HTTP que admita 'byte range requests' los ficheros .mpd, y también habrá que alojar la página web desde la que se reproducirán los vídeos. 

	- Usamos Apache2 como servidor local para alojar tanto la página web donde se reproducirán los vídeos como los archivos .mpd y .webm
	Ejemplo de contenido en el servidor: 
		/var/www/html# ls
		audio_48k-final.webm             video_160x90_250k_final.webm
		index.html                       video_320x180_500k_final.webm
		index_original.html              video_640x360_1000k_final.webm
		my_video_manifest.mpd            video_640x360_750k_final.webm
		video_1280x720_1500k_final.webm

