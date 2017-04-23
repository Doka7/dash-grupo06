#!/usr/bin/python
import os, sys
from termcolor import colored

if sys.argv [1] == "-e":

	try:
		argumento = sys.argv[2]

	except:
		sys.exit("Se necesita un segundo argumento que diga el nombre del archivo a codificar.")

	aux = str(argumento);
	clip_name = aux.partition(".")[0] #quitamos la extension para guardar en el servidor un nombre del clip indentificativo. 
	#print(colored(clip_name, 'green'))


	#codificacion del clip seleccionado en el argumento.
	os.system("ffmpeg -i /home/doka/Escritorio/alex/dash/public/videos/original/" + argumento + " -c:v libvpx-vp9 -f webm -dash 1 -an -s 160x90 -b:v 250k /home/doka/Escritorio/alex/dash/public/videos/aux/" + clip_name + "_160x90_250k.webm -y")
	os.system("ffmpeg -i /home/doka/Escritorio/alex/dash/public/videos/original/" + argumento + " -c:v libvpx-vp9 -f webm -dash 1 -an -s 320x180 -b:v 500k /home/doka/Escritorio/alex/dash/public/videos/aux/" + clip_name + "_320x180_500k.webm -y")
	os.system("ffmpeg -i /home/doka/Escritorio/alex/dash/public/videos/original/" + argumento + " -c:v libvpx-vp9 -f webm -dash 1 -an -s 640x360 -b:v 750k /home/doka/Escritorio/alex/dash/public/videos/aux/" + clip_name + "_640x360_750k.webm -y")
	os.system("ffmpeg -i /home/doka/Escritorio/alex/dash/public/videos/original/" + argumento + " -c:v libvpx-vp9 -f webm -dash 1 -an -s 1280x720 -b:v 1500k /home/doka/Escritorio/alex/dash/public/videos/aux/" + clip_name + "_1280x720_1500k.webm -y")
	os.system("ffmpeg -i /home/doka/Escritorio/alex/dash/public/videos/original/" + argumento + " -acodec libopus -vn -ar 48k /home/doka/Escritorio/alex/dash/public/audios/aux/" + clip_name + "_48k.webm -y")

	#mkvmuxer para alinear los clusters y habilitar el switching de calidades. 	
	os.system("/home/doka/Descargas/libwebm/mkvmuxer_sample -i /home/doka/Escritorio/alex/dash/public/videos/aux/" + clip_name + "_1280x720_1500k.webm -o /home/doka/Escritorio/alex/dash/public/videos/codec/" + clip_name + "_1280x720_1500k.webm")
	os.system("/home/doka/Descargas/libwebm/mkvmuxer_sample -i /home/doka/Escritorio/alex/dash/public/videos/aux/" + clip_name + "_640x360_750k.webm -o /home/doka/Escritorio/alex/dash/public/videos/codec/" + clip_name + "_640x360_750k.webm")
	os.system("/home/doka/Descargas/libwebm/mkvmuxer_sample -i /home/doka/Escritorio/alex/dash/public/videos/aux/" + clip_name + "_320x180_500k.webm -o /home/doka/Escritorio/alex/dash/public/videos/codec/" + clip_name + "_320x180_500k.webm")
	os.system("/home/doka/Descargas/libwebm/mkvmuxer_sample -i /home/doka/Escritorio/alex/dash/public/videos/aux/" + clip_name + "_160x90_250k.webm -o /home/doka/Escritorio/alex/dash/public/videos/codec/" + clip_name + "_160x90_250k.webm")
	os.system("/home/doka/Descargas/libwebm/mkvmuxer_sample -i /home/doka/Escritorio/alex/dash/public/audios/aux/" + clip_name + "_48k.webm -o /home/doka/Escritorio/alex/dash/public/audios/codec/" + clip_name + "_48k.webm -output_cues 1 -cues_on_audio_track 1 -max_cluster_duration 2 -audio_track_number 0")

	#creacion del manifest donde se referencian los clips con las distintas calidades. 
	os.chdir("/home/doka/Escritorio/alex/dash/public")
	#print(colored(os.getcwd(), 'green'))
	os.system("/home/doka/Descargas/webm-tools/webm_dash_manifest/webm_dash_manifest -o " + clip_name + "_manifest.mpd -as id=0,lang=eng -r id=1,file=videos/codec/" + clip_name + "_1280x720_1500k.webm -r id=2,file=videos/codec/" + clip_name + "_640x360_750k.webm -r id=3,file=videos/codec/" + clip_name + "_320x180_500k.webm -r id=4,file=videos/codec/" + clip_name + "_160x90_250k.webm -as id=1,lang=eng -r id=5,file=audios/codec/" + clip_name + "_48k.webm")

elif sys.argv [1] == "-h":

	print "-encode: codifica el archivo que se desee en varios formatos para reproducirlo con distintas calidades en funcion de las prestaciones. IMPORTANTE: el clip seleccionado debe estar en /home/doka/Escritorio/alex/dash/public/videos/original/"

else: 	
	sys.exit("Elige un comando existente, usa info para saber los comandos que se pueden usar.")