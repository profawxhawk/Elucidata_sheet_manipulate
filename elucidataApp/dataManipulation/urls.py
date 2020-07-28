from django.urls import path

from dataManipulation import views as dM_views

urlpatterns = [
    path('', dM_views.home, name='home'),
    path('/', dM_views.home, name='home'),
    path('/file_upload',dM_views.upload_file,name='upload_file')
]