
from django.conf import settings
from django.shortcuts import render,redirect
from .forms import DocumentForm
from .models import Document
from .mojiart import main as mojiartfunc
from PIL import Image
from io import BytesIO
import base64
 
def index(request):
    form = DocumentForm()
    params = {
        'form': form,
    }
    if request.method == 'POST':
        form = DocumentForm(request.FILES, request.FILES)
        if form.is_valid():
            #form.save()
            if 'submit' in request.POST:
                img = form.cleaned_data['img']
                msk = form.cleaned_data['msk']
                params['obj'] = func(img, msk)
                print("aaa")
            return render(request, 'upload/index.html', params)
    else:
        form = DocumentForm()
    return render(request, 'upload/index.html', params)

def base64save(img):
    buffer = BytesIO() # メモリ上への仮保管先を生成
    img.save(buffer, format="PNG")
    base64Img = base64.b64encode(buffer.getvalue()).decode().replace("'", "")
    return base64Img


def func(img, msk):
    #image = mojiartfunc(img, msk)
    image = Image.open(img)
    return base64save(image)
