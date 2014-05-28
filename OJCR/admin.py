from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib import admin
from OJCR.models import User,CodeEntry
from django.contrib.auth.admin import UserAdmin

class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','is_active', 'is_superuser',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField(label= ("Password"),
        help_text= ("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))
    
    class Meta:
        model = User
        fields = ('email', 'is_staff', 'is_active', 'is_superuser','password')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UsersAdmin(UserAdmin):
    
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('id', 'email','is_staff','is_active','is_superuser',)
    list_filter = ('is_staff','is_active','is_superuser',)
    
    fieldsets = (
        (None, {
                'classes': ('wide',),
                'fields': ('email', 'is_staff','is_active','is_superuser','password')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','is_staff','is_active','is_superuser')}
        ),
    )
        
    ordering = ['id']
    search_fields = ('email',)
    
    
class CodeRepoAdmin(admin.ModelAdmin):
    
    list_display = ('id','owner', 'className', 'message','createdOn','lastModify')
    list_filter = ('createdOn',)
    ordering = ['-createdOn']
    search_fields = ('className','message')
    date_hierarchy = 'createdOn'
    
admin.site.register(User,UsersAdmin)
admin.site.register(CodeEntry,CodeRepoAdmin)