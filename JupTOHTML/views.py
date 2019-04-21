import mimetypes
import os
from subprocess import  call
import zipfile
from wsgiref.util import FileWrapper

import nbformat
from django.template import Context
from django.utils.encoding import smart_str
from nbconvert import HTMLExporter

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, Http404
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from JupyterToHTML import settings


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

    def post(self, request):
        if request.FILES['uploadedFile']:
            myfile = request.FILES['uploadedFile']
            fs = FileSystemStorage()

            filename = fs.save(str(myfile.name).replace(" ","_"), myfile)

            path = settings.MEDIA_ROOT + "/" + filename
            print ("jupyter nbconvert --to HTML "+path)
            os.system("jupyter nbconvert --to HTML "+path)
            htmlFile = str(filename).replace("ipynb","html")
            path = str(path).replace("ipynb","html")
            #response = download(request, path)
            context = Context()
            context['FIleInDownload'] = htmlFile
        return render(request, 'index.html', context.flatten())



def download(request):
    # download and delete file
    file_name = request.GET.get('file_name')
    file_path = settings.MEDIA_ROOT + "/" + file_name
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404



# def processZip(path,pk=""):
#
#     # z = zipfile.ZipFile()   ### I am unsure of what goes here!!
#     # probably should do some logic on the name and file type
#     # or be very aware of what is in the zip file
#     with zipfile.ZipFile(path, 'r') as z:
#         for f in z.namelist():
#             images.update({f: base64.b64encode(z.read(f)),})
#
#     context = {
#         "images": images,
#         }
#     template_name = 'photos/detail.html'
#     return render(request,template_name,context)

