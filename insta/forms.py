from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from insta.models import UserModel


class ImageForm(forms.Form):
	image = forms.ImageField()

class PostForm(forms.Form):
    image = forms.ImageField()
    caption = forms.CharField()

class BioForm(forms.Form):
    bio = forms.CharField()

class ProfileForm(forms.Form):
    profile_name = forms.CharField()

class LoginForm(forms.Form):    
		username = forms.CharField()
		password = forms.CharField(widget=forms.PasswordInput)
		widgets = {
			'password': forms.PasswordInput(),
		}

		class Meta:
			fields = ['username','password']

class SignupForm(forms.ModelForm):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Signup'))

    class Meta:
        model = UserModel        
        password = forms.CharField(widget=forms.PasswordInput)        
        widgets = {
            'password': forms.PasswordInput(),
        }       
        fields = ['username','email','profile_name','password']

