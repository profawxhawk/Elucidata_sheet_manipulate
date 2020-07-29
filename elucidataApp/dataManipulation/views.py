from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse
from .forms import UploadFileForm
from .models import File
import pandas as pd
import zipfile
from io import BytesIO
# Create your views here.
def home(request):
    form = UploadFileForm()
    return render(request, 'DataManipulation/homepage.html',{'form':form})

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form_model = form.save(commit=False)
            form_model.save()
            request.session['path']=str(form_model.File.url)
            return render(request, 'DataManipulation/menupage.html',{'success':True,'name':form.cleaned_data['File']})
        else:
            form = UploadFileForm()
            return render(request, 'DataManipulation/homepage.html',{'form':form,'error':True})

    else:
        return redirect(reverse('home'))

def Task_1(request):
    if request.session['path']:
        df=pd.read_excel(request.session['path'][1:])
        
        df_PC=df[df['Accepted Compound ID'].str.contains("PC",na=False)]
        df_PC=df_PC[~df_PC["Accepted Compound ID"].str.contains("LPC",na=False)]
        df_PC=df_PC[~df_PC["Accepted Compound ID"].str.contains("plasmalogen",na=False)]
        df_LPC=df[df['Accepted Compound ID'].str.contains("LPC",na=False)]
        df_plasmalogen=df[df['Accepted Compound ID'].str.contains("plasmalogen",na=False)]

        output = BytesIO()
        f = zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED)
        f.writestr("PC_IDS.csv",df_PC.to_csv())
        f.writestr("LPC_IDS.csv",df_LPC.to_csv())
        f.writestr("plasmalogen_IDS.csv",df_plasmalogen.to_csv())
        f.close()
        
        response = HttpResponse(output.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="Task1.zip"'
        return response
