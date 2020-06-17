from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Sponsor, Reference

from django.forms.widgets import ClearableFileInput

class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = get_user_model()
        #fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
        fields = ('email', 'password1', 'password2')#, 'first_name', 'last_name','citizenship', 'address', 'city', 'province', 'postal', 'country')
           #'research_interests', 'phd_institute', 'phd_year')

class EditProfileForm(forms.ModelForm):
#class EditProfileForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'last_name', 
            'citizenship', 'current_institute', 'address', 'city', 'province', 'postal', 'country', 
        )


class EducationProfileForm(forms.ModelForm):
#class EditProfileForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = (
            'phd_institute', 'phd_year', 'research_interests',
        )

class SelectSponsorForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            'sponsor_1',
            'sponsor_2',
        )


class UploadFileForm(forms.ModelForm):
    #template_name='/something/else'
    #resume = forms.FileField()
    #research_statement = forms.FileField()
    resume = forms.FileField(label='Resume',  widget=ClearableFileInput)
    research_statement = forms.FileField(label='research_statement',  widget=ClearableFileInput)

    ClearableFileInput.template_name = "widgets/custom_clearable_file_input.html"

    #company_logo = forms.ImageField(label=_('Company Logo'),required=False, error_messages = {'invalid':_("Image files only")})

    class Meta:
        model = get_user_model()
        fields = ('resume', 'research_statement')

class UploadResumeForm(forms.ModelForm):
    #template_name='/something/else'
    #resume = forms.FileField()
    #research_statement = forms.FileField()
    resume = forms.FileField(label='Resume',  widget=ClearableFileInput)
    #research_statement = forms.FileField(label='research_statement',  widget=ClearableFileInput)

    ClearableFileInput.template_name = "widgets/custom_clearable_file_input.html"

    #company_logo = forms.ImageField(label=_('Company Logo'),required=False, error_messages = {'invalid':_("Image files only")})

    class Meta:
        model = get_user_model()
        fields = ('resume',)#, 'research_statement')

class UploadResearchStatementForm(forms.ModelForm):
    research_statement = forms.FileField(label='Research statement',  widget=ClearableFileInput)
    ClearableFileInput.template_name = "widgets/custom_clearable_file_input.html"

    class Meta:
        model = get_user_model()
        fields = ('research_statement',)#'resume')

class UploadPublicationForm(forms.ModelForm):
    publication = forms.FileField(label='Publication list',  widget=ClearableFileInput)
    ClearableFileInput.template_name = "widgets/custom_clearable_file_input.html"

    class Meta:
        model = get_user_model()
        fields = ('publication',)#'resume')

class SponsorAddForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        fields = ('email', 'first_name', 'last_name', 'institute')

class SponsorListForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        fields = ('email', 'first_name', 'last_name', 'institute')


class RefAddForm(forms.ModelForm):
    class Meta:
        model = Reference
        fields = ('name', 'email')


class RefLetterUploadForm(forms.ModelForm):
    letter = forms.FileField(label='letter',  widget=ClearableFileInput)
    ClearableFileInput.template_name = "widgets/custom_clearable_file_input.html"
    class Meta:
        model = Reference
        fields = ('letter',)