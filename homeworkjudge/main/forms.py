from django import forms

from .models import Student


class studentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Student
        fields =[
            'studentId',
            'password',
            'studentName',
        ]