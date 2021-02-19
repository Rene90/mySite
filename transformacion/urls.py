from django.urls import path
from . import views
app_name = 'transformacion'

urlpatterns=[
    path('',views.AboutView.as_view(),name="about"),
    path('transformar/',views.ConvertView,name="convert"),
    #path('resultados/<object_id>/',views.ResultadoView.as_view(),kwargs=dict(model=models.userModel), name="resultados")


]
