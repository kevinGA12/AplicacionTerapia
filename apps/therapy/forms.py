from django import forms
from .models import Sessions, Threads, Posts, Profiles, Resources


class therapyForm(forms.ModelForm):
    class Meta:
        model = Sessions
        fields = ['description', 'category', 'doctor', 'therapy_date', 'therapy_time']

class NewThreadForm(forms.ModelForm):
    class Meta:
        model = Threads
        fields = ['title', 'initial_post']

class NewPostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['message']
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profiles
        fields = ['age', 'currentmood', 'wellbeing', 'stresslevel', 'anxietylevel']

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resources
        fields = ['title', 'text', 'icon', 'category']

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
