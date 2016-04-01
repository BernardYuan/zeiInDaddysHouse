from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import connection
from django.core import serializers
from bbjjzl.models import group as Group
from bbjjzl.models import music as Music
import base64
import hashlib
import os

def index(request):
    return render(request, 'bbjjzl/index.html')

def user_new(request) :
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.POST['username'])
            return JsonResponse({'status': 1})
        except:
            try:
                user = User.objects.get(email=request.POST['email'])
                return JsonResponse({'status': 2})
            except:
                user = User.objects.create_user(username=request.POST['username'],
                                         email=request.POST['email'],
                                         password=request.POST['password'])
                user.save()
                return JsonResponse({'status': 0})

def user_login(request) :
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        request.session['id'] = user.id
        if user.is_active:
            return JsonResponse({'status': 0})
        else:
            return JsonResponse({'status': 1})
    else :
        return JsonResponse({'status': 2})

def group_new(request) :
    if request.method == "POST":
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO bbjjzl_group (name, uid, proPic, description, nSong, songList) VALUES('" + request.POST["name"] + "', " + str(request.session["id"]) + ", '" + request.POST["proPic"] + "', '" + request.POST["description"] + "', 0, '[]');")
        except:
            return HttpResponse("Creating group failed!")
        finally:
            cursor.close()
            return HttpResponse("Creating group succeeded!")

    return render(request, 'bbjjzl/group_new.html')

def group_home(request) :
    return render(request, 'bbjjzl/group_home.html')

def upload(request):
    if request.method == "POST":
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO bbjjzl_music (name, artist, vHash) VALUES('" + request.POST["name"] + "', " + request.POST["artist"] + "', '" + request.POST["vHash"] + "');")
        except:
            return HttpResponse("Creating music failed!")
        finally:
            cursor.close()

        idSong = Music.objects.values("id").filter(hash = request.POST["vHash"])

        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE bbjjzl_group set nSong = nSong + 1;")
        except:
            return HttpResponse("The number of songs update failed!")
        finally:
            cursor.close()

        Music.addSong(idSong["id"])
        return HttpResponse("haha")

    return render(request, 'bbjjzl/upload.html')


def file_upload(request) :
    if request.method == "POST":
        """database select and insert example
        instance = Group.objects.values('name').filter(name = 'Jericho')
        return JsonResponse(instance[0], safe=False)"""

        # base64 decode
        if request.POST['file'].index(','):
            filedata = base64.b64decode(request.POST['file'][request.POST['file'].index(',') + 1:])
        else:
            filedata = base64.b64decode(request.POST['file'])

        # get hash value
        filehash = hashfile(filedata)

        # create the folder if it doesn't exist.
        filepath = settings.BASE_DIR + '/bbjjzl/static/uploads/' + filehash[:2]
        try:
            os.mkdir(filepath)
        except:
            pass

        filepath = filepath + '/' + filehash[2:4]
        try:
            os.mkdir(filepath)
        except:
            pass

        # write file to disk
        fout = open(filepath + '/' + filehash[4:], 'wb')
        try:
            fout.write(filedata)
            fout.close()
            return JsonResponse({'status': 0, 'hash': filehash})
        except:
            return JsonResponse({'status': 1, 'message': 'image saving failed'})

def hashfile(f):
    sha1 = hashlib.sha1()

    sha1.update(f)

    return sha1.hexdigest()

