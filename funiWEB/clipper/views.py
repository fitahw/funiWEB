from django.shortcuts import render
from django.http import JsonResponse, FileResponse
import yt_dlp
from yt_dlp.utils import download_range_func
import os
import subprocess
import multitasking
import time
# Create your views here.


def index(request):
    return render(request, 'clipper.html')

@multitasking.task
def deleteClip(path):
    time.sleep(380)
    os.remove(path)

@multitasking.task
def ajaxData(request):
    if request.method == "POST":
        url = request.POST.get('YTurl')
        urlHash = request.POST.get('uqUrl')
        time1 = request.POST.get('time1')
        time2 = request.POST.get('time2')
        path = f'clips/{urlHash}.mp4'

        deleteClip(path)
        ''''
        with yt_dlp.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(url, download=False)
            filenameDirt = info_dict.get('title', None)
            filename = "_".join(filenameDirt.split())
        '''

        ydl_opts = {
            'outtmpl': path,
            'format': 'b',
            'verbose': True,
            'download_ranges': download_range_func(None, [(time1, time2)]),
            'force_keyframes_at_cuts': True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download(url)
            except:
                print('Error in downloading video')
                try:
                    ydl_opts_v = {
                        'outtmpl': path[:-4] + '_v.mp4',
                        'format': '299',
                        'download_ranges': download_range_func(None, [(time1, time2)]),
                        'force_keyframes_at_cuts': True,
                        'postprocessors': [{
                            'key': 'FFmpegVideoConvertor',
                            'preferedformat': 'mp4'
                        }]
                    }

                    ydl_opts_a = {
                        'outtmpl': path[:-4] + '_a',
                        'format': '251',
                        'download_ranges': download_range_func(None, [(time1, time2)]),
                        'force_keyframes_at_cuts': True,
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio'
                        }, {
                            'key': 'FFmpegFixupM4a'
                        }]
                    }

                    ydlV = yt_dlp.YoutubeDL(ydl_opts_v)
                    ydlA = yt_dlp.YoutubeDL(ydl_opts_a)
                    file = ydlV.download(url)
                    file2 = ydlA.download(url)

                    commannd = f"ffmpeg -i {path[:-4] + '_v.mp4'} -i {path[:-4] + '_a.opus'} -c:v copy -c copy {path}"
                    subprocess.call(commannd, shell=True, cwd='')

                    os.remove(path[:-4] + '_v.mp4')
                    os.remove(path[:-4] + '_a.opus')
                except:
                    return JsonResponse({'success': False})

            if os.path.exists(path):
                print('Video already downloaded')
                return FileResponse(open(path, 'rb'), as_attachment=True, filename=f'{urlHash}.mp4')
            else:
                print('Video not downloaded')
                return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': False})
