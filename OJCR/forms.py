 # -*- coding: utf-8 -*-
 
from django import forms
from django.core.exceptions import ValidationError
import re

class LoginForm(forms.Form):
   
    email = forms.EmailField(
                             label='پست الکترونیک',
                             error_messages={    'required': 'لطفا ایمیل خود را وارد کنید',
                                                 'invalid': 'ایمیل وارد شده معتبر نمی باشد'})
    
    password = forms.CharField(
                               widget=forms.PasswordInput,
                               label='رمز عبور',
                               error_messages={    'required': 'لطفا رمز عبور خود را وارد کنید',
                                                 'invalid': 'رمز عبور وارد شده معتبر نمی باشد'})
def validate_class_name(value):
    
    validation_result = re.match(r'^(([a-zA-Z][a-zA-Z_$0-9]*(\.[a-zA-Z][a-zA-Z_$0-9]*)*)\.)?([a-zA-Z][a-zA-Z_$0-9]*)$', value)
    if not validation_result:
        raise ValidationError(u'نام کلاس معتبر نمیباشد')
    
class AddEditForm(forms.Form):
       
    className = forms.CharField(validators=[validate_class_name],max_length=100,
                               label='نام کلاس',
                               error_messages={    'required': 'لطفا نام کلاس را وارد کنید',
                                                 'invalid': 'نام کلاس معتبر نمی باشد'})
    message = forms.CharField(max_length=250,
                               widget=forms.Textarea,
                               label='متن قابل چاپ',
                               error_messages={    'required': 'لطفا متن پیام را وارد کنید',
                                                 'invalid': 'متن پیام معتبر نمی باشد'})
    
    