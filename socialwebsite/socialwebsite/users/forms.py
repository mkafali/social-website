from typing import Any
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo','bio','private')

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':''}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':''}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':''}))


	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = ''
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = ''
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = ''
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError("This mail adress has already registered.")
		return email
     
class UserProfileUpdateForm(UserChangeForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email Adresin'}),required=False)
    first_name = forms.CharField(label="", max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'adın'}),required=False)
    last_name = forms.CharField(label="", max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'soyad'}),required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

		

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
		
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists() and self.instance.email!=email:
              raise forms.ValidationError("This mail adress has already exist")
        return email


class PasswordReset(forms.Form):
	new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput)
	new_password2 = forms.CharField(label="New Password Confirmation", widget=forms.PasswordInput)
      
	#def clean_password(self):
	#	if self.new_password1!=self.new_password2:
	#		raise forms.ValidationError("Password Confirmation is wrong")
      
class ForgotMyPassword(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}),required=True)
    mail = forms.EmailField(label="Mail", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your Mail Adress'}),required=True)
    
class PasswordMailCode(forms.Form):
    mail_code = forms.CharField(label="Code", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Code'}),required=True)
    
class ComplainProfileForm(forms.Form):
    reason = forms.CharField(label="Your Reason",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your Reason'}),required=True)
      
class HaveProblemForm(forms.Form):
    title = forms.CharField(label="Title",max_length=20,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your Reason'}),required=True)
    reason = forms.CharField(label="Reason",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your Reason'}),required=True)