from django import forms

class availabilityForm(forms.Form):
    start_date = forms.DateField(label='Lease Date', widget=forms.SelectDateWidget)
    end_date = forms.DateField(label='clear_date', widget=forms.SelectDateWidget)

class customerForm(forms.Form):
    first_name = forms.CharField(max_length=150, label='First Name')
    last_name = forms.CharField(max_length=150, label='Last Name')
    date_of_birth = forms.DateField(label='Date of Birth', widget=forms.SelectDateWidget)
    email = forms.CharField(max_length=150, label='email')
    phone_number = forms.CharField(max_length=150, label="phone_number")

class confirmForm(forms.Form):
    pass