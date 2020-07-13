from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.template.loader import get_template
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages

import os
import pyaudio
import wave
import sys
import multiprocessing as mp

from essentia import *
from essentia.standard import *

from songcollection import SongCollection
from tracklister import TrackLister
from djcontroller import DjController
import essentia
from colorlog import ColoredFormatter

import logging
# Create your views here.
def upload(request):
    if request.method == "POST":
        myfile = request.FILES.get('myfile',  None)
        if not myfile :
            return HttpResponse("No file for upload")
        destination = open(os.path.join("/home/ddman/音樂/upload/", myfile.name), 'wb+')
        for chunk in myfile.chunks():
            destination.write(chunk)
        destination.close()
        return HttpResponse("upload over!")
    return render(request, "DJ.html", locals())

# def upload_file(request):
#     if request.method == 'POST':
#         form = Song(request.POST, request.FILES)
#         if form.is_valid():#表單資料如果合法
#             handle_uploaded_file(request.FILES['file'])#處理上傳來的檔案
#             return HttpResponse('檔案上傳成功！')
#         else:
#             form = Song()
#     return render(request, 'DJ.html', {'form':form})

# def handle_uploaded_file(f):
#     today = str(datetime.date.today())#獲得今天日期
#     file_name = today   '_'   f.name#獲得上傳來的檔名稱,加入下劃線分開日期和名稱
#     file_path = os.path.join(os.path.dirname(__file__),'upload_file',file_name)#拼裝目錄名稱 檔名稱
#     with open(file_path, 'wb ') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)    
def  get_sound(a):
    while len(data)>0:
        CHUNK=1024
        p = pyaudio.PyAudio()
        wf = wave.open('/home/ddman/音樂/EDM_2/Body_feat__brando_Extended_Mix.wav')
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                                    channels=wf.getnchannels(),
                                    rate=wf.getframerate(),
                                    output=True)
        data = wf.readframes(CHUNK)
        stream.write(data)
    return data
def  test(request):
    temp = 0
    # CHUNK = 1024
    # wf = wave.open('/home/ddman/音樂/EDM_2/Body_feat__brando_Extended_Mix.wav', 'rb')
    # stream = ''
    # data = ''
    # instantiate PyAudio (1)
    # p = pyaudio.PyAudio()
    if request.method == "POST":
        temp = request.POST.get('test',  None)
        if temp == '1' :
            a = mp.Process(target=get_sound, args=(1,))
            a.start()
            return render(request,"test_1.html",locals())
            # open stream (2)
            # stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
            #                 channels=wf.getnchannels(),
            #                 rate=wf.getfp = pyaudio.PyAudio()
            # # read data
            # data = wf.readframes(CHUNK)
            # return render(request,"test_1.html",locals())
            # # play stream (3)
            # while len(data) > 0:
            #     stream.write(data)
            #     data = wf.readframes(CHUNK)

            # # stop stream (4)
            # stream.stop_stream()
            # stream.close()

            # # close PyAudio (5)
            # p.terminate()
            # return render(request,"test_1.html",locals())
        else :
            stream = 0
            return render(request,"test_1.html",locals())
    return render(request,"test_1.html",locals())
def index_dj(request):
    template = get_template("Index.html")
    LOG_LEVEL = logging.DEBUG
    LOGFORMAT = "%(log_color)s%(message)s%(reset)s"
    logging.root.setLevel(LOG_LEVEL)
    formatter = ColoredFormatter(LOGFORMAT)
    stream = logging.StreamHandler()
    stream.setLevel(LOG_LEVEL)
    stream.setFormatter(formatter)
    logger = logging.getLogger('colorlogger')
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(stream)
	
    sc = SongCollection()
    tl = TrackLister(sc)
    dj = DjController(tl)
	
    essentia.log.infoActive = False
    essentia.log.warningActive = False
    
    if request.method == "POST":
        cmd = request.POST.get("cmd", None)
        cmd = str(cmd)
        # cmd_split = str(cmd).split
        # cmd = cmd_split[0]
        while(True):
                # try:
                #     cmd_split = str.split(input('> : '), ' ')
                # except KeyboardInterrupt:
                #     logger.info('Goodbye!')
                #     break
                # cmd = cmd_split[0]
            # if cmd == 'loaddir':
            #     if len(cmd_split) == 1:
            #         return HttpResponse('Please provide a directory name to load!')
            #         continue
            #     elif not os.path.isdir(cmd_split[1]):
            #         return HttpResponse(cmd_split[1] + ' is not a valid directory!')
            #         continue
            message = "abc"
            sc.load_directory("/home/ddman/音樂/upload")
            message = str(len(sc.songs)) + ' songs loaded [annotated: ' + str(len(sc.get_annotated())) + ']'
            if cmd == 'play':
                if len(sc.get_annotated()) == 0:
                    message = 'Use the loaddir command to load some songs before playing!'
                    continue
                    
                # if len(cmd_split) > 1 and cmd_split[1] == 'save':
                #     message = 'Saving this new mix to disk!'
                #     save_mix = True
                # else: 
                #     save_mix = False
                            
                message = 'Starting playback!'
                try:
                    dj.play(save_mix=False)
                except Exception as e:
                    logger.error(e)
                return render(request, "Index.html", locals())
            elif cmd == 'pause':
                message = 'Pausing playback!'
                try:
                    dj.pause()
                except Exception as e:
                    logger.error(e)
                return render(request, "Index.html", locals())
            elif cmd == 'skip' or cmd == 's':
                message = 'Skipping to next segment...'
                try:
                    dj.skipToNextSegment()
                except Exception as e:
                    logger.error(e)
                return render(request, "Index.html", locals())
            elif cmd == 'stop':
                message = 'Stopping playback!'
                dj.stop()
                return render(request, "Index.html", locals())
            elif cmd == 'save':
                message = 'Saving the next new mix!'
                return render(request, "Index.html", locals())
            elif cmd == 'showannotated':
                message = 'Number of annotated songs ' + str(len(sc.get_annotated()))
                message = 'Number of unannotated songs ' + str(len(sc.get_unannotated()))
                return render(request, "Index.html", locals())
            elif cmd == 'annotate':
                message = 'Started annotating!'
                sc.annotate()
                message = 'Done annotating!'
                return render(request, "Index.html", locals())
            elif cmd == 'debug':
                LOG_LEVEL = logging.DEBUG
                logging.root.setLevel(LOG_LEVEL)
                stream.setLevel(LOG_LEVEL)
                logger.setLevel(LOG_LEVEL)
                message = 'Enabled debug info. Use this command before playing, or it will have no effect.'
                return render(request, "Index.html", locals())
            elif cmd == 'mark':
                dj.markCurrentMaster()
                return render(request, "Index.html", locals())
            elif cmd == "quit" :
                break
                return render(request, "Index.html", locals())
            else:
                message = 'The command ' + str(cmd) + ' does not exist!'
                return render(request, "Index.html", locals())
    return render(request, "Index.html", locals())