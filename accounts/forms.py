from django import forms

from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', max_length=30)
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False)
        label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
        label='Password (again)')
    
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username__iexact=username)
            raise forms.ValidationError(u'Username is already taken')
        except User.DoesNotExist:
            pass
        return username
    
    def clean(self):
        if ('password1' in self.cleaned_data and 'password2' in 
            self.cleaned_data):
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 != password2:
                raise forms.ValidationError(
                    u'You must type the same password each time')
        return self.cleaned_data
    
    def save(self):
        return User.objects.create_user(self.cleaned_data['username'],
            '', self.cleaned_data['password1'])

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        # Short circuit if they haven't entered in their password
        if not username or not password:
            return self.cleaned_data
        try:
            self.user = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            raise forms.ValidationError(u'Invalid username and/or password')
        if not self.user.check_password(password):
            raise forms.ValidationError(u'Invalid username and/or password')
        return self.cleaned_data