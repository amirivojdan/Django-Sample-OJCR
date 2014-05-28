 # -*- coding: utf-8 -*-
 
from django.shortcuts import render_to_response,redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import logout,authenticate, login,get_user_model
from django.template import RequestContext
from django.utils import timezone
from OJCR.models import User, CodeEntry, UserManager 
from OJCR.forms import LoginForm, AddEditForm

def login_register(request):
    
    if request.user.is_authenticated():
        return redirect('home')
    
    if request.method == 'POST': 
        
        submitted_form = LoginForm(request.POST)
        if submitted_form.is_valid():
            submitted_email = submitted_form.cleaned_data['email']
            submitted_password = submitted_form.cleaned_data['password']
            if '_loginButton_' in request.POST :

                loged_in_user = authenticate(username=submitted_email, password=submitted_password)
                if loged_in_user == None:
                    return render_to_response('OJCR/login.html',{'form': submitted_form,'login_error': 'نام کاربری و یا رمز عبور صحیح نمیباشد !',},context_instance=RequestContext(request))
                if loged_in_user.is_active:
                    login(request, loged_in_user)
                    return redirect('home')
                
                else :                
                    return render_to_response('OJCR/login.html',{'form': submitted_form,'login_error': 'حساب کاربری شما مسدود می باشد !',},context_instance=RequestContext(request)) 
            
            elif '_registerButton_' in request.POST:
                get_user_model().objects.create_user(submitted_email,submitted_password)
                registered_user = authenticate(username=submitted_form.cleaned_data['email'], password=submitted_form.cleaned_data['password'])
                login(request,registered_user)
                return redirect('home')
            else:
                return redirect('login_register')
        else : 
            return render_to_response('OJCR/login.html',{'form': submitted_form},context_instance=RequestContext(request))
    else :
        raw_login_form = LoginForm()
        return render_to_response('OJCR/login.html',{'form': raw_login_form},context_instance=RequestContext(request))         
    # else go login show error  

def do_logout(request):
    logout(request)
    return redirect('login_register')

@login_required(login_url=settings.LOGIN_URL)
def home(request):
   
    loged_in_user_entries = CodeEntry.objects.filter(owner=request.user)     
    return render_to_response('OJCR/home.html', {'items':loged_in_user_entries}, context_instance=RequestContext(request))

@login_required(login_url=settings.LOGIN_URL)
def edit_class(request,id):
    if request.method == 'GET': 
        try:
            requested_code_entry = CodeEntry.objects.get(id=id)
            if requested_code_entry.owner == request.user:
                filled_edit_form = AddEditForm(initial={'className': requested_code_entry.className,'message': requested_code_entry.message})
                return render_to_response('OJCR/add_edit.html',{'form':filled_edit_form,'select':'edit'},context_instance=RequestContext(request))        
            return redirect('home')    
        except CodeEntry.DoesNotExist:
            return redirect('home')
    else:
        
        try:
            requested_code_entry = CodeEntry.objects.get(id=id)
            if '_cancel_btn' in request.POST :
                return redirect('home')
            submitted_form = AddEditForm(request.POST)
            if submitted_form.is_valid():
                    if requested_code_entry.owner == request.user:
                        
                        requested_code_entry.className = submitted_form.cleaned_data['className'] 
                        requested_code_entry.message = submitted_form.cleaned_data['message']    
                        requested_code_entry.lastModify = timezone.now() 
                        requested_code_entry.save()
            else:
                return render_to_response('OJCR/add_edit.html', {'form':submitted_form, 'select':'edit'}, context_instance=RequestContext(request))     
            return redirect('home')    
        except CodeEntry.DoesNotExist:
            return redirect('home')
        

@login_required(login_url=settings.LOGIN_URL)
def add_class(request):

    if request.method == 'POST': 
        submitted_form = AddEditForm(request.POST)
        if '_cancel_btn' in request.POST :
            return redirect('home')
        if submitted_form.is_valid():
            submitted_className = submitted_form.cleaned_data['className']
            submitted_message = submitted_form.cleaned_data['message']
            created_code_entry = CodeEntry(owner=request.user, className=submitted_className, message=submitted_message)
            created_code_entry.save()
            return redirect('home')
        else:
            return render_to_response('OJCR/add_edit.html', {'form':submitted_form,'select':'add'}, context_instance=RequestContext(request))  
    else:
        raw_edit_form = AddEditForm()
        return render_to_response('OJCR/add_edit.html', {'form':raw_edit_form, 'select':'add'},context_instance=RequestContext(request))

@login_required(login_url=settings.LOGIN_URL)
def download_class(request, id):
    try:
        requested_code_entry = CodeEntry.objects.get(id=id)
        if requested_code_entry.owner == request.user:
            
            return requested_code_entry.get_archived_response()
        
        else:
            return redirect('home')    
    except CodeEntry.DoesNotExist:
        return redirect('home')
    
    
    return render_to_response('OJCR/404.html',context_instance=RequestContext(request))

@login_required(login_url=settings.LOGIN_URL)
def remove_class(request, id):
    try:
        requested_code_entry = CodeEntry.objects.get(id=id)
        if requested_code_entry.owner == request.user:
            requested_code_entry.delete()
        
        return redirect('home')    
    except CodeEntry.DoesNotExist:
        return redirect('home')
        
    

