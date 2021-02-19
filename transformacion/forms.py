from django import forms
from . import models
# creating a form
class ConvertForm(forms.Form):
    #latitud = forms.FloatField(required=False)
    #longitud = forms.FloatField(required=False)
    #altura = forms.FloatField(required=False)
    #equis = forms.FloatField(required=False)
    #ye = forms.FloatField(required=False)
    #zeta = forms.FloatField(required=False)
    #class Meta():
    #    model = models.Transformacion
    #    fields = '__all__'
    latitud = forms.FloatField(required=False,label="Latitud")
    longitud = forms.FloatField(required=False,label="Longitud")
    altura = forms.FloatField(required=False,label="Altura")
    equis = forms.FloatField(required=False,label="X")
    ye = forms.FloatField(required=False,label="Y")
    zeta = forms.FloatField(required=False,label="Z")
