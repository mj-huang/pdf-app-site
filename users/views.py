from django.contrib.auth import login as auth_login
from django.contrib.auth import get_user_model

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

#from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError

from django.urls import reverse

from django.conf import settings

from .forms import (
    SignUpForm, 
    EditProfileForm, 
    EducationProfileForm,
    UploadFileForm,
    SponsorAddForm, 
    SponsorListForm,
    SelectSponsorForm,
    UploadResumeForm,
    UploadResearchStatementForm,
    UploadPublicationForm,
    RefAddForm,
    RefLetterUploadForm,
)

from .models import User, Sponsor, Reference

# Create your views here.
@csrf_protect
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            #return HttpResponseRedirect('/profile/edit/')
            #return redirect('profile_edit', pk=request.user.id)
            return redirect('profile_edit')
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})

#@login_required
def welcom_view(request):#):
    user = request.user
    item_list = ['Email', 'First name', 'Last name', 'Citizenship', 'Address', 'City', 'Province', 'Postal', 'Country', 'Phd Institute', 'PhD Year', 'Research Interests' ]
    #args = {'user': user}
    return render(request, 'welcom.html', {'user': user, 'item_list': item_list})

#@register.simple_tag
@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            #return HttpResponseRedirect('/profile/upload/')
            return redirect('profile_education')

    else:
        form = EditProfileForm(instance=request.user)
        #form = EditProfileForm()
    return render(request, 'profile_edit.html', {'form': form, 'profile_edit': "active"})

@login_required
def profile_education(request):
    if request.method == 'POST':
        form = EducationProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            #return HttpResponseRedirect('/profile/upload/')
            return redirect('profile_select_sponsor')

    else:
        form = EducationProfileForm(instance=request.user)

    return render(request, 'profile_education.html', {'form': form, 'profile_education': 'active'})


@login_required
def profile_select_sponsor(request):
    if request.method == 'POST':
        form = SelectSponsorForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile_upload_file')

    else:
        form = SelectSponsorForm(instance=request.user)
        #form = EditProfileForm()
    return render(request, 'profile_select_sponsor.html', {'form': form, 'profile_select_sponsor': 'active'})

@login_required
def profile_upload_file(request):
    form_resume = UploadResumeForm(prefix="resume", instance=request.user)
    form_research_statement = UploadResearchStatementForm(prefix="research_statement", instance=request.user)
    form_publication = UploadPublicationForm(prefix="publication", instance=request.user)

    if request.method == 'POST':
        #print( request.POST )
        #print(  len(list( request.FILES.keys() )) )

        if "btn_resume" in request.POST:
            form_resume = UploadResumeForm(request.POST, request.FILES, prefix="resume", instance=request.user)
            if form_resume.is_valid() :
                form_resume.save()
                return redirect('profile_upload_file')

        elif "btn_research_statement" in request.POST:
            form_research_statement = UploadResearchStatementForm(request.POST, request.FILES, prefix="research_statement", instance=request.user)
            if form_research_statement.is_valid() :
                form_research_statement.save()
                return redirect('profile_upload_file')
        
        elif "btn_publication" in request.POST:
            form_publication = UploadPublicationForm(request.POST, request.FILES, prefix="publication", instance=request.user)
            if form_publication.is_valid() :
                form_publication.save()
                return redirect('profile_upload_file')

    return render(request, 'profile_upload_file.html', {'form_resume': form_resume, 'form_research_statement': form_research_statement, 'form_publication': form_publication, 'profile_upload_file': 'active'} )


@login_required
def profile_reference(request):
    #print(request.user.id)

    def send_ref_email(form, ref_label, current_scheme_host):
        #if getattr(form, 'is_valid') :
        if form.is_valid():
            user = request.user # get user object of logged in user

            ref = form.save(commit=False) # save corresponding user for a reference
            ref.user = user
            ref.save()

            ref_name = form.cleaned_data['name']
            subject = 'Send out TEST email ' + ref_name
            from_email = 'mjthebes@gmail.com'
            message = current_scheme_host + reverse('ref_upload', kwargs={'pk': ref.id})
            to_email = form.cleaned_data['email']

            send_mail(subject, message, from_email, [to_email]) # send email to reference
            ref.sent = True # label True when email was sent
            ref.save()

            setattr(user, ref_label, ref) # save ref_label-th reference in user model
            user.save()

            return ref.sent

    user = request.user

    form_ref_1 = RefAddForm(instance=user.ref_1)
    form_ref_2 = RefAddForm(instance=user.ref_2)
    form_ref_3 = RefAddForm(instance=user.ref_3)
    btn_ref_list = ['btn_ref_1', 'btn_ref_2', 'btn_ref_3']

    if request.method == 'POST':
        print(request.POST)
        ref_list = ['ref_1', 'ref_2', 'ref_3']
        #form_list = ['','','']

        for i, (ref, btn_ref) in enumerate( zip(ref_list,btn_ref_list ) ):
            if btn_ref in request.POST:
                form = RefAddForm(request.POST)
                send_ref_email(form, ref, request._current_scheme_host)

        return redirect('profile_reference')

    ref_sent_list = []
    form_ref_zip_list = []
    user_ref_list = [user.ref_1, user.ref_2, user.ref_3]
    form_ref_list = [form_ref_1, form_ref_2, form_ref_3]
    refs_list = [ ['Reference 1', ''], ['Reference 2', ''], ['Reference 3', ''] ]

    for form_ref, user_ref, refs in zip(form_ref_list, user_ref_list, refs_list):
        try :
            ref_sent = user_ref.sent
        except :
            ref_sent = False
        print(ref_sent)
        #refs = ['Reference 1', '']
        ref_sent_list.append(ref_sent)
        letter_sent = [ref_sent, ref_sent]
        #form_ref_1_zip = zip(form_ref, refs, letter_sent)
        form_ref_zip_list.append(zip(form_ref, refs, letter_sent))

    form_ref_zip = zip(btn_ref_list, ref_sent_list, form_ref_zip_list )

    return render( request, 'profile_reference.html', {'form_ref_zip': form_ref_zip, 'profile_reference': 'active'} )


@login_required
def profile_view(request):#):
    #if pk:
    #    user = User.objects.get(pk=pk)
    #else:
    #    
    user = request.user
    item_list = ['Email', 'First name', 'Last name', 'Citizenship', 'Address', 'City', 'Province', 'Postal', 'Country', 'Phd Institute', 'PhD Year', 'Research Interests' ]
    #args = {'user': user}
    return render(request, 'profile_summary.html', {'user': user, 'item_list': item_list, 'profile_summary': 'active'})


def ref_upload(request, pk):
    reference = Reference.objects.get(pk=pk)

    if request.method == 'POST':
        #print(request.id)
        reference = Reference.objects.get(pk=pk)
        form = RefLetterUploadForm(request.POST, request.FILES, instance=reference)
        #print(form)
        #form = RefAddForm(request.POST)
        if form.is_valid():
            ref = form.save(commit=False)
            ref.received = True
            ref.save()
            #pass
            #form.save()
        
        return redirect('ref_upload', pk=pk)
    else:
        form = RefLetterUploadForm(instance=reference)

    return render(request, 'ref_upload.html', {'ref': reference, 'form':form})

def ref_list(request):
    refs = Reference.objects.all()
    return render(request, 'ref_list.html', {'refs': refs})



def sponsor_add(request):
    if request.method == 'POST':
        form = SponsorAddForm(request.POST)
        #form = EditProfileForm(request.POST)

        if form.is_valid():
            form.save()
            #return HttpResponseRedirect('/profile/upload/')
            return redirect('sponsor_list')

    else:
        form = SponsorAddForm()
        #form = EditProfileForm()
    return render(request, 'sponsor_add.html', {'form': form, 'profile_select_sponsor': 'active'})



def sponsor_list(request):
    sponsors = Sponsor.objects.all()
    return render(request, 'sponsor_list.html', {'sponsors': sponsors})



