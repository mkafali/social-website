from .models import Post, Comment
from django import forms

class PhotoPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('image','caption','title')

class PhotoPostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('caption','title')

class ConfirmPasswordForm(forms.Form):
    your_password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_your_password = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput)

class ComplainPostForm(forms.Form):
    reason = forms.CharField(label="Your Reason",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your Reason'}),required=True)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class ComplainCommentForm(forms.Form):
    reason = forms.CharField(label="Your Reason",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your Reason'}),required=True)