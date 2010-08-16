from django import forms

from tail.models import ServerTail

class ServerTailForm(forms.Form):
    hostname = forms.CharField(max_length=50)
    port = forms.IntegerField(initial=22)
    username = forms.CharField(max_length=50)
    password = forms.CharField(
        widget=forms.PasswordInput(render_value=False),
        required=False,
        label='Password (optional)',
    )
    path = forms.CharField(max_length=255)
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        if self.user:
            if not self.user.is_authenticated():
                self.user = None
        super(ServerTailForm, self).__init__(*args, **kwargs)
    
    def save(self):
        st, created = ServerTail.objects.get_or_create(
            hostname=self.cleaned_data['hostname'],
            port=self.cleaned_data['port'],
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            path=self.cleaned_data['path'],
            user=self.user,
        )
        return st