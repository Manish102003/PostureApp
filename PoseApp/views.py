from django.shortcuts import  render
from django.contrib.auth.decorators import login_required
from user.forms import ImageForm
from django.shortcuts import get_object_or_404,redirect,get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
import app
from user.models import Image

@login_required
def index(request):
    if request.method == "POST":
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            image_url = image.image.url
            result = app.posture(image_url[1:])
            image.status = result['status']
            image.problems = "".join(result['problems'])
            image.exercises = "".join(result['exercises'])
            image.save()
            return redirect('/')
    else:
        image = ImageForm()
    return render(request,'index.html',{"image":image})

@login_required
def result(request):
    images = Image.objects.filter(user=request.user)
    return render(request,"home.html",{"images":images})
