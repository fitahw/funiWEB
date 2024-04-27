from django.shortcuts import render
from django.http import JsonResponse, FileResponse
import yt_dlp
import os
# Create your views here.


def index(request):
    return render(request, 'clipper.html')


def ajaxData(request):
    if request.method == "POST":
        url = request.POST.get('YTurl')
        urlHash = url[32:]
        ''''
        with yt_dlp.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(url, download=False)
            filenameDirt = info_dict.get('title', None)
            filename = "_".join(filenameDirt.split())
        '''

        path = f'clips/{urlHash}.mp4'
        ydl_opts = {
            'outtmpl': path,
            'format': 'b',
            # 'download_ranges': download_range_func(None, [(time1, time2)]),
            #'force_keyframes_at_cuts': True,
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
                return JsonResponse({'success': False})

            if os.path.exists(path):
                print('Video already downloaded')
                return FileResponse(open(path, 'rb'), as_attachment=True, filename=f'{urlHash}.mp4')
            else:
                print('Video not downloaded')
                return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': False})
