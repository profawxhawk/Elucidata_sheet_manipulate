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
    else:
        return redirect(reverse('home'))

def Task_2(request):
    
    if request.session['path']:
        df=pd.read_excel(request.session['path'][1:])
        df['Retention Time Roundoff (in mins)']=df['Retention time (min)'].round().astype(int)

        temp_columns=df.columns.tolist()
        temp_columns.insert(3,temp_columns[-1])
        temp_columns=temp_columns[:len(temp_columns)-1]
        df=df[temp_columns]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Task2.csv'

        df.to_csv(path_or_buf=response,index=False)
        return response
    else:
        return redirect(reverse('home'))

def Task_3(request):
    if request.session['path']:
        df=pd.read_excel(request.session['path'][1:])
        df['Retention Time Roundoff (in mins)']=df['Retention time (min)'].round().astype(int)

        temp_columns=df.columns[3:len(df.columns)].tolist()
        temp_columns.insert(0,temp_columns[-1])
        temp_columns=temp_columns[:len(temp_columns)-1]
        df=df.groupby(['Retention Time Roundoff (in mins)'])[temp_columns].mean()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Task3.csv'

        df.to_csv(path_or_buf=response,index=False)
        return response
    else:
        return redirect(reverse('home'))
