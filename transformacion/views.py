from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import forms
import folium

import math
def index(lat,lon):
    start_coords = (lat, lon)
    folium_map = folium.Map(
        location=start_coords,
        zoom_start=12,
        tiles="cartodbpositron",
        width='100%',
        height='100%'
    )
    tooltip = "Haz click"
    folium.Marker([lat, lon], popup="<i>Aquí estoy<i/>", tooltip=tooltip, icon= folium.Icon(color='red',icon='info-sign')).add_to(folium_map)

    my_map=folium_map._repr_html_()

    return my_map
def calcN(a,b,phi):
    arriba = a**2
    abajo = (((a**2)*math.cos(phi)**2)+((b**2)*math.sin(phi)**2))**.5
    return arriba/abajo
def grados2rad(angulo):
    return angulo * math.pi/180
def conversiongeo2cart(phi,lam,h,a,b):
    phi = grados2rad(phi)
    lam = grados2rad(lam)
    N = calcN(a,b,phi)
    x =(N+h)* math.cos(phi)*math.cos(lam)
    y =(N+h)* math.cos(phi)*math.sin(lam)
    z =((N*(b**2/a**2))+h) * math.sin(phi)
    return x,y,z
def conversioncart2geo(x,y,z,a,b):
    Longitud =math.atan(y/x)
    Longitud = Longitud*180/math.pi-180
    e2= 1-(b**2/a**2)
    p= (x**2+y**2)**.5
    N_ =a
    h_ = (x**2+y**2+z**2)**.5-(a*b)**.5
    phi_ = math.atan((z/p)*(1-(e2*N_/(N_+h_)))**-1)
    condicion = True
    i = 0
    while condicion:
        Ni = a/(math.cos(phi_)**2+((b**2/a**2)*math.sin(phi_)**2))**.5
        hi = (p/math.cos(phi_))-Ni
        phii= math.atan((z/p)*(1-(e2*Ni/(Ni+hi)))**-1)
        condicion = (abs(hi-h_)>a*10e-20) and (abs(phii-phi_)>10e-20)
        h_ =hi
        phi_ = phii
        i = i+1
    phi_ = phi_*180/math.pi
    return phi_,Longitud,h_


class AboutView(TemplateView):
    template_name = "transformacion/transformacion_about.html"

class ResultadoView(TemplateView):
    def myfunction(self,request, object_id, **kwargs):
        model = kwargs['model']

def ConvertView(request):
    a = 6378137.0
    b = 6356752.314245
    context = {}
    form = forms.ConvertForm(request.POST or None)
    context['form'] = form
    if request.POST:
        if form.is_valid():

            if(form.cleaned_data.get('latitud') and abs(form.cleaned_data.get('latitud')) >0 and abs(form.cleaned_data.get('latitud')) <90 and form.cleaned_data.get('longitud') and abs(form.cleaned_data.get('longitud')) >0 and abs(form.cleaned_data.get('longitud')) <180 and form.cleaned_data.get('altura') and abs(form.cleaned_data.get('altura')) >=0 ):
                print ("Adios")
                x,y,z =conversiongeo2cart(form.cleaned_data.get('latitud'),form.cleaned_data.get('longitud'),form.cleaned_data.get('altura'),a,b)
                mapa = index(form.cleaned_data.get('latitud'),form.cleaned_data.get('longitud'))
                equiss = [{'lat':form.cleaned_data.get('latitud'),'lon':form.cleaned_data.get('longitud'),'h':form.cleaned_data.get('altura'),'x':x,'y':y,'z':z,'mapa':mapa}]

                return render(request, 'transformacion/transformacion_resultados.html',{'equiss':equiss})
            if(form.cleaned_data.get('equis') and form.cleaned_data.get('ye') and form.cleaned_data.get('zeta') ):
                phi,la,ha= conversioncart2geo(form.cleaned_data.get('equis'),form.cleaned_data.get('ye'),form.cleaned_data.get('zeta'),a,b)

                mapa =index(phi,la)
                equiss = [{'lat':phi,'lon':la,'h':ha,'x':form.cleaned_data.get('equis'),'y':form.cleaned_data.get('ye'),'z':form.cleaned_data.get('zeta'),'mapa':mapa}]

                return render(request, 'transformacion/transformacion_resultados.html',{'equiss':equiss})
            mapa = index(19.5,-99.9)
            equiss = [{'lat':form.cleaned_data.get('latitud'),'lon':form.cleaned_data.get('longitud'),'h':form.cleaned_data.get('altura'),'x':form.cleaned_data.get('equis'),'y':form.cleaned_data.get('ye'),'z':form.cleaned_data.get('zeta'),'mapa':mapa}]
            #return HttpResponseRedirect(reverse('transformacion:resultados',kwargs=from.cleaned_data))
            print ("Goood")

            return render(request, 'transformacion/transformacion_resultados.html',{'equiss':equiss})
    else:
        form = forms.ConvertForm()
    context['form'] = form
    return render(request, "transformacion/transformacion_form.html",context)

# Create your views here.
