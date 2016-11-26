"""AuthenticationApp Forms

Created by Naman Patwari on 10/4/2016.
"""
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import MyUser, Student, Professor, Engineer
from tinymce.widgets import TinyMCE

class LoginForm(forms.Form):
    email = forms.CharField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

USERS = (
    ('STU','Student'),
    ('PRO','Professor'),
    ('ENG','Engineer'),
)

UNIVS = (
    ('BSU','Ball State University'),
    ('PU','Purdue University'),
    ('ND','University of Notre Dame'),
)

class RegisterForm(forms.Form):
    """A form to creating new users. Includes all the required
    fields, plus a repeated password."""
    email = forms.CharField(label='Email', widget=forms.EmailInput, required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=True)    

    firstname = forms.CharField(label="First name", widget=forms.TextInput, required=False)
    lastname = forms.CharField(label="Last name", widget=forms.TextInput, required=False)

    usertype = forms.ChoiceField(label="Account type", choices=USERS, required=True)

    univ = forms.ChoiceField(label="University (or alma mater)", choices=UNIVS, required=True)
    about = forms.CharField(label="About me", widget=TinyMCE(attrs={'cols': 80, 'rows': 10}), required=False)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get("email")
        #Check if email exists before
        try:
            exists = MyUser.objects.get(email=email)
            raise forms.ValidationError("This email has already been taken")
        except MyUser.DoesNotExist:
            return email
        except:
            raise forms.ValidationError("There was an error, please contact us later")

class UpdateForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['usertype'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = MyUser
        # if (usertype == 'Student'):
        #     fields = ('email', 'password', 'first_name', 'last_name', 'university', 'about')
        # if (usertype == 'Professor'):
        #     fields = ('email', 'password', 'first_name', 'last_name', 'university', 'about')
        # if (usertype == 'Engineer'):
        #     fields = ('email', 'password', 'first_name', 'last_name', 'universtiy', 'about')
        fields = ('email', 'password', 'first_name', 'last_name', 'univ', 'usertype', 'about')

    def clean_password(self):            
        return self.initial["password"]  

    def clean_usertype(self):
        return self.initial["usertype"]      

    def clean_about(self):
        return self.cleaned_data.get("about")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        #Check is email has changed
        if email == self.initial["email"]:
            return email
        #Check if email exists before
        try:
            exists = MyUser.objects.get(email=email)
            raise forms.ValidationError("This email has already been taken")
        except MyUser.DoesNotExist:
            return email
        except:
            raise forms.ValidationError("There was an error, please contact us later")

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        #Check is email has changed
        if first_name is None or first_name == "" or first_name == '':  
            email = self.cleaned_data.get("email")                               
            return email[:email.find("@")]      
        return first_name
   


"""Admin Forms"""

class AdminUserCreationForm(forms.ModelForm):
    """A form for Admin to creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)    

    class Meta:
        model = MyUser
        fields = ('email', 'first_name', 'last_name')        

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(AdminUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for Admin for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        #fields = ('email', 'password', 'first_name', 'last_name', 'is_active', 'is_admin')
        fields = ('email', 'password', 'first_name', 'last_name', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]   
