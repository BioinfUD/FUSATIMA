# -*- coding: utf-8 -*-
from forms import *
from processing.models import *
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.template import loader, Context, RequestContext
from django.contrib.auth import authenticate, login, logout
from django.core.servers.basehttp import FileWrapper
import os
from PIL import Image


#   ############ AUTENTICATION ###############
def auth_view(request):
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    user = authenticate(username=email, password=password)
    if user is not None:
        login(request, user)
        profile = User.objects.select_related().get(id=request.user.pk).profile
        uploadFiles = File.objects.filter(
            profile=profile).filter(tipo=1).order_by("-id")[:5]
        procesos = Proceso.objects.filter(profile=profile).order_by("-id")[:5]
        return render(request, 'home.html', {'profile': profile, 'uploadFiles': uploadFiles, 'procesos': procesos})
    else:
        error = 'No se ha podido acceder, intente nuevamente'
        return render(request, 'error.html', {'error': error})


def error_login(request):
    error = 'El ususario o la contraseña son incorrectos'
    return render(request, 'error.html', {'error': error})


def log_in(request):
    return render(request, 'login.html')


def log_out(request):
    logout(request)
    success = 'Ha cerrado sesión satisfactoriamente. Si desdea acceder de nuevo haga clic en el siguiente botón:'
    url_continuar = '/login'
    msg_continuar = 'Acceder a la cuenta'
    return render(request, 'success.html', {'success': success, 'url_continuar': url_continuar, 'msg_continuar': msg_continuar})


#  ############ REGISTRATION ###############
def register_user(request):
    if request.POST:
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        if password1 == password2:
            try:
                if User.objects.filter(username=email):
                    error = 'El usuario ya existe'
                    return render(request, 'error.html', {'error': error})
                else:
                    new_user = User(username=email, email=email)
                    new_user.set_password(password1)
                    new_user.save()
                    new_profile = Profile(user=new_user,
                                          email=email,
                                          firstName=request.POST.get('firstName', ''),
                                          lastName=request.POST.get('lastName', ''),
                                          )
                    new_profile.save()
                    # Agrego los 5 archivos predeterminados al usuario
                    testFiles = File.objects.filter(test=True)
                    for f in testFiles:
                        url_file = f.fileUpload.url
                        new_test_file = File(fileUpload=Django_File(open("%s%s" % (settings.BASE_DIR, url_file))),
                                             description="Archivo de Prueba", profile=new_profile, ext="results", tipo=1)
                        new_test_file.save()
                    success = 'Se ha registrado satisfactoriamente.'
                    url_continuar = '/login'
                    msg_continuar = 'Acceder a la cuenta'
                    return render(request, 'success.html', {'success': success, 'url_continuar': url_continuar, 'msg_continuar': msg_continuar})
            except:
                error = 'Error al registrar intente de nuevo'
                return render(request, 'error.html', {'error': error})
        else:
            error = 'Las contrasenas no son iguales'
            return render(request, 'error.html', {'error': error})
    else:
        return render(request, 'register.html')


#  ############ FILES ###############

@login_required(login_url='/login/')
def filesubmit(request):
    if request.method == 'POST':
        #  try:
        desc = request.POST.get('description', '')
        tipo_imagen = True if request.POST.get('tipo', '') == "Multiespectral" else False
        user = User.objects.select_related().get(id=request.user.pk)
        p = user.profile
        ext = str(request.FILES['file']).split(".")[-1]
        instance = File(fileUpload=request.FILES[
                        'file'], description=desc, profile=p, ext=ext, tipo=1, tipo_multi=tipo_imagen)
        instance.save()
        outfile = instance.fileUpload.path + ".jpg"
        print outfile
        try:
            im = Image.open(os.path.join(instance.fileUpload.path))
            print "Generating jpeg for %s" % instance.fileUpload.path
            im.thumbnail(im.size)
            im.save(outfile, "JPEG", quality=100)
        except Exception, e:
            print e
        success = 'El archivo se ha guardado satisfactoriamente.'
        url_continuar = '/files'
        msg_continuar = 'Ver lista de archivos'
        return render(request, 'success.html', {'success': success, 'url_continuar': url_continuar, 'msg_continuar': msg_continuar})
        #  except Exception as e:
        #    print e
    else:
        return render(request, 'upload.html')


@login_required(login_url='/login/')
def delete_file(request, fileID):
    try:
        file2del = File.objects.get(id=int(fileID))
        profile = ser = User.objects.select_related().get(id=request.user.pk).profile
        if file2del.profile == profile:
            file2del.delete()
            success = 'Se ha eliminado el archivo satisfactoriamente.'
            url_continuar = '/files'
            msg_continuar = 'Ver lista de archivos'
            return render(request, 'success.html', {'success': success, 'url_continuar': url_continuar, 'msg_continuar': msg_continuar})
        else:
            error = 'Este archivo no le pertenece'
            return render(request, 'error.html', {'error': error})
    except Exception, e:
        return render(request, 'error.html', {'error': e})


@login_required(login_url='/login/')
def show_fileupload(request):
    form = UploadFileForm()
    return render(request, 'fileupload.html', {'form': form})


@login_required(login_url='/login/')
def show_edit_file(request, fileID):
    return render(request, 'show_edit_file.html', {'fileID': fileID})


@login_required(login_url='/login/')
def editfile(request):
    desc = request.POST.get('description', '')
    fileID = request.POST.get('fileid', '')

    try:
        profile = User.objects.select_related().get(id=request.user.pk).profile
        instance = File.objects.get(id=int(fileID))
        instance.description = desc
        instance.save()
        success = 'Se ha editado el archivo satisfactoriamente.'
        url_continuar = '/files'
        msg_continuar = 'Ver lista de archivos'
        return render(request, 'success.html', {'success': success, 'url_continuar': url_continuar, 'msg_continuar': msg_continuar})
    except Exception, e:
        error = 'No se pudieron guardar los datos'
        return render(request, 'error.html', {'error': error})


#  ############ PAGE RENDER ###############
def home(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = ImagesForm(request.POST)
            if form.is_valid():
                pass# Hago cosas:
        # if a GET (or any other method) we'll create a blank form
        else:
            profile = User.objects.select_related().get(id=request.user.pk).profile
            pan_image_files = File.objects.all().filter(profile=profile).filter(tipo=1).filter(tipo_multi=False)
            mul_image_files = File.objects.all().filter(profile=profile).filter(tipo=1).filter(tipo_multi=True)
            return render(request, 'home.html', {'pan_image_files': pan_image_files, 'mul_image_files': mul_image_files})
    else:
        return render(request, 'home.html')


def show_video(request):
    return render(request, 'video.html')


def show_tutorial(request):
    image_data = open('%s/Manuales/ManualUsuarioFusionMultiPan.pdf' % settings.BASE_DIR, 'rb').read()
    return HttpResponse(image_data, content_type='application/pdf')


@login_required(login_url='/login/')
def upload_success(request):
    success = 'Se ha subido el archivo satisfactoriamente.'
    return render(request, 'success.html', {'success': success})


@login_required(login_url='/login/')
def show_files(request):
    user = User.objects.select_related().get(id=request.user.pk)
    profile = user.profile
    mul_file_list = File.objects.all().filter(profile=profile).filter(tipo=1).filter(tipo_multi=True).order_by("-id")
    pan_file_list = File.objects.all().filter(profile=profile).filter(tipo=1).filter(tipo_multi=False).order_by("-id")
    return render(request, 'files.html', {'pan_file_list': pan_file_list, 'mul_file_list': mul_file_list})


@login_required(login_url='/login/')
def show_process(request):
    user = User.objects.select_related().get(id=request.user.pk)
    profile = user.profile
    processes = Proceso.objects.all().filter(profile=profile).order_by("-id")
    return render(request, 'processes.html', {'process_list': processes})


@login_required(login_url='/login/')
def show_error_process(request, process_id):
    p = Proceso.objects.get(id=process_id)
    return render(request, 'proccess_error.html', {'p': p})


@login_required(login_url='/login/')
def show_processes(request):
    return render(request, 'show_processes.html')


#  Show standard err and output of process
@login_required(login_url='/login/')
def show_specific_process(request, process_id):
    p = Proceso.objects.get(id=process_id)
    return render(request, 'show_process_info.html', {'p': p})


@login_required(login_url='/login/')
def download_file(request, id_file):
    file_path = File.objects.get(id=id_file).fileUpload.path
    wrapper = FileWrapper(file(file_path))
    filename = file_path.split("/")[-1]
    response = HttpResponse(wrapper, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    response['Content-Length'] = os.path.getsize(file_path)
    print os.path.getsize(file_path)
    print file_path
    return response

########## RUN THE FUSION SCRIPT ################


@login_required(login_url='/login/')
def make_fusion(request):
    file_id = request.POST.get('file', '')
    file_path = File.objects.get(id=int(file_id)).fileUpload.path
    k = request.POST.get('k', '')
    numKmers = request.POST.get('numKmers', '')
    profile = User.objects.select_related().get(id=request.user.pk).profile
    bf = BFCounter(contador=0, k=k, numKmers=numKmers, profile=profile)
    bf.save()
    bf.run(file=file_path, k=k, numKmers=numKmers)
    success = 'El proceso se ha enviado a ejecución, para ver su estado, consulte la lista de procesos por meido del boton "Procesos" del menú principal o haciendo clic en el siguiente botón:'
    url_continuar = '/process/show'
    msg_continuar = 'Ver lista de procesos'
    return render(request, 'success.html', {'success': success, 'url_continuar': url_continuar, 'msg_continuar': msg_continuar})

