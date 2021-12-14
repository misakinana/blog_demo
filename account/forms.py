from django import forms
from django.contrib.auth.models import User

class AccountForm(forms.Form):
    user_name = forms.CharField()
    user_password = forms.CharField()

class AccountRegisterForm(forms.ModelForm):
    password = forms.CharField()
    password2 = forms.CharField()
    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("两次密码输入不一致，请重新输入。")
