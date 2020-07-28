from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import UploadFileForm
from .models import File
# Create your views here.
def home(request):
    form = UploadFileForm()
    return render(request, 'DataManipulation/homepage.html',{'form':form})

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form_model=File()
            form_model.Name = form.cleaned_data["Name"]
            form_model.File = form.cleaned_data["File"]
            form_model.save()
            form = UploadFileForm()
            return render(request, 'DataManipulation/homepage.html',{'form':form,'success':True})
        else:
            form = UploadFileForm()
            return render(request, 'DataManipulation/homepage.html',{'form':form,'error':True})

    else:
        return redirect(reverse('home'))
