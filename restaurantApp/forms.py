from django import forms
from restaurantApp.models import *


class DateInput(forms.DateInput):
    input_type = 'date'

class DateForm(forms.Form):
    date_field = forms.DateField(widget=DateInput)

class ReservationForm(forms.ModelForm):
    # pass
    class Meta():
        model = Reservation
        fields = ['date', 'time_start', 'time_end']

        widgets = {
            'date': forms.DateInput(attrs={'type':'date'}),
            'time_start': forms.TimeInput(attrs={'type': 'time'}),
            'time_end': forms.TimeInput(attrs={'type': 'time'})
        }


