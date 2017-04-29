PASOS SEGUIDOS PARA INSTALACIÓN DE SERVIDOR/CLIENTE DASH: 
https://developer.mozilla.org/en-US/docs/Web/HTML/DASH_Adaptive_Streaming_for_HTML_5_Video

1. INSTALACIÓN DE HERRAMIENTAS NECESARIAS

1.1 FFMPEG

	Descarga de FFmpeg para la codificación de audio/vídeo en distintos formatos de calidad que se almacenarán en el servidor.

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



1.2 MKV_MUXERSAMPLE

	Instalar libwebm, concretamente nos interesa la herramienta mkv_muxersample para agrupar alinear los diferentes flujos multimedia generados, habilitando así el switching de calidades más adelante. Básicamente se ocupa de que todos los GOP sigan el mismo formato.

	Para instalar: 
		- git clone https://chromium.googlesource.com/webm/libwebm
		- renombrar el Makefile.unix a Makefile y ejecutar 'make'

	Ejemplo de uso: 
	./mkvmuxer_sample -i video_1280x720_1500k.webm -o video_1280x720_1500k_final.webm
	./mkvmuxer_sample -i audio_48k.webm -o audio_48k_final.webm -output_cues 1 -cues_on_audio_track 1 -max_cluster_duration 2 -audio_track_number 0



1.3 WEB_DASH_MANIFEST

	Instalar webm-tools, concretamente para instalar la herramienta 'webm_dash_manifest' que permite crear archivos .mpd 

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

	Para comprobar si un archivo MPD es correcto, existen validators como: http://www-itec.uni-klu.ac.at/dash/?page_id=605



1.4 PATHS RELATIVOS PARA EJECUTAR LAS HERRAMIENTAS

	Añadir al final del archivo ~/.bashrc los paths de las carpetas que contienen los programas instalados, en mi caso están serían: 

		export PATH=$PATH:/home/doka/Descargas/webm-tools/webm_dash_manifest
		export PATH=$PATH:/home/doka/Descargas/libwebm

	Esto permite ejecutar dichas herramientas desde cualquier sitio, sin necesidad de que en el script de python aparezcan rutas absolutas a las herramientas. De este modo el script es facilmente ejecutable desde cualquier ordenador. 


2. GENERACIÓN DE ESPACIO DE TRABAJO. EXPRESS. 

	Para generar la estructura de directorios que permita el correcto funcionamiento del script, así como para facilitar el trabajo en grupo al subir toda esta estructura común a GitHub, utilizamos Express. 

	Seguir los pasos indicados en: https://expressjs.com/en/starter/installing.html

3. EJECUCIÓN DEL SCRIPT encoder.py

	El script mencionado genera automáticamente las distintas representaciones del contenido audiovisual que se indique como parámetro, además del fichero manifest correspondiente. El archivo a codificar debe estar almacenado en public/videos/original. 

	Ejemplo de uso: ./encoder.py -e clip_monza.mp4

	Tras su ejecución, la aplicación podrá lanzarse con el comando node bin/www, y podrá accederse desde cualquier navegador web en el puerto 3000. 





