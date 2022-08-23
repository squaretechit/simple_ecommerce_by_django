from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.hashers import check_password


class LoginForm(forms.Form):

    username = forms.CharField(label="Username ",
                               error_messages={'required': 'Enter a valid Username.'},
                               max_length=50,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Username',
                                   'class': 'form-control'
                               }))

    password = forms.CharField(label="Password ",
                               error_messages={'required': 'Password Required.'},
                               min_length=8,
                               max_length=50,
                               widget=forms.PasswordInput(attrs={
                                   'placeholder': 'Password',
                                   'class': 'form-control'
                               }))

    def clean_username(self):
        data = self.cleaned_data['username']
        if not User.objects.filter(username=data).exists():
            raise ValidationError("Username Dose not Match!!")
        return data

    def clean(self):
        cleaned_data = super().clean()
        login_password = cleaned_data.get("password")
        if login_password:
            username = cleaned_data.get("username")
            try:
                users_current_password = User.objects.filter(username=username).first()
                if not check_password(login_password, users_current_password.password):
                    self.add_error('password', "Wrong Password. Please try again!!!")
            except:
                pass


class RegisterForm(forms.Form):

    chooseCountry = [
        ('Germany', 'Germany')
    ]

    first_name = forms.CharField(label="First Name?",
                                 error_messages={'required': 'First Name Required.'},
                                 max_length=100,
                                 widget=forms.TextInput(attrs={
                                     'placeholder': 'First Name',
                                     'class': 'form-control'
                                 })
                                 )

    last_name = forms.CharField(label="Last Name?",
                                error_messages={'required': 'Last Name Required.'},
                                max_length=100,
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'Last Name',
                                    'class': 'form-control'
                                })
                                )

    username = forms.CharField(label="Username?",
                               error_messages={'required': 'Username Required.'},
                               max_length=100,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Username',
                                   'class': 'form-control'
                               }))

    phone_number = forms.CharField(label="Phone number?",
                                   error_messages={'required': 'Phone number Required.'},
                                   max_length=100,
                                   widget=forms.NumberInput(attrs={
                                       'placeholder': 'Phone Number',
                                       'class': 'form-control'
                                   }))

    email = forms.EmailField(label="Email?",
                             error_messages={'required': 'Valid Email Required.'},
                             max_length=100,
                             help_text='We will send you a email to this email.',
                             widget=forms.EmailInput(attrs={
                                 'placeholder': 'Email',
                                 'class': 'form-control'
                             }))

    country = forms.CharField(label='Country / Region',
                              widget=forms.Select(
                                  choices=chooseCountry,
                                  attrs={'class': 'd-block selectcountry'
                                         }))

    street = forms.CharField(label="Street?",
                             error_messages={'required': 'Street Required.'},
                             max_length=100,
                             widget=forms.TextInput(attrs={
                                 'placeholder': 'Street',
                                 'class': 'form-control'
                             }))

    postcode = forms.CharField(label="Postcode?",
                               error_messages={'required': 'Postcode Required.'},
                               max_length=100,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Postcode',
                                   'class': 'form-control'
                               }))

    city = forms.CharField(label="City?",
                           error_messages={'required': 'City Required.'},
                           max_length=100,
                           widget=forms.TextInput(attrs={
                               'placeholder': 'City',
                               'class': 'form-control'
                           }))

    password = forms.CharField(label="Password?",
                               error_messages={'required': 'Password Required.'},
                               min_length=8,
                               max_length=50,
                               widget=forms.PasswordInput(attrs={
                                   'placeholder': 'Password',
                                   'class': 'form-control'
                               }))

    confirm_password = forms.CharField(label="Confirm Password?",
                                       error_messages={'required': 'Password Required.'},
                                       min_length=8,
                                       max_length=50,
                                       widget=forms.PasswordInput(attrs={
                                           'placeholder': 'Confirm Password',
                                           'class': 'form-control'
                                       }))

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise ValidationError("Username already exists.")
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise ValidationError("Email already exists.")
        return data

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password:
            if password != confirm_password:
                error = "Password Did not Match!!"
                self.add_error('password', error)
                self.add_error('confirmPassword', error)


class PassChangeForm(PasswordChangeForm):

    old_password = forms.CharField(required=True,
                                   label='Old Password',
                                   widget=forms.PasswordInput(attrs={
                                       'placeholder': 'Old Password'
                                   }),
                                   error_messages={
                                       'required': 'Old Password is required.'}
                                   )

    new_password1 = forms.CharField(required=True,
                                    label='New Password',
                                    widget=forms.PasswordInput(attrs={
                                        'placeholder': 'New Password'
                                    }),
                                    error_messages={'required': 'New Password is required.'},
                                    min_length=8,
                                    max_length=50)

    new_password2 = forms.CharField(required=True,
                                    label='Confirm Password',
                                    widget=forms.PasswordInput(attrs={
                                        'placeholder': 'Confirm Password'
                                    }),
                                    error_messages={'required': 'Confirm Password is required.'},
                                    min_length=8,
                                    max_length=50)


class PassResetEmailForm(PasswordResetForm):

    email = forms.EmailField(required=True,
                             label='Email',
                             widget=forms.EmailInput(attrs={
                                 'placeholder': 'Enter a valid email'
                             }),
                             error_messages={'required': 'Enter A Valid Email.'}
                             )
    
    def clean_email(self):
        data = self.cleaned_data['email']
        if not User.objects.filter(email=data).exists():
            raise ValidationError("This Email dose not exists!")
        return data


class PassRestForm(forms.Form):

    password = forms.CharField(required=True,
                               label='New Password',
                               widget=forms.PasswordInput(attrs={
                                   'placeholder': 'New Password'
                               }),
                               error_messages={'required': 'New Password required.'},
                               min_length=8,
                               max_length=50
                               )

    confirm_password = forms.CharField(required=True,
                                       label='Confirm Password',
                                       widget=forms.PasswordInput(attrs={
                                           'placeholder': 'Confirm Password'
                                       }),
                                       error_messages={'required': 'Confirm Password required.'},
                                       min_length=8,
                                       max_length=50
                                       )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password:
            if password != confirm_password:
                error = "Password Did not Match!!"
                self.add_error('password', error)
                self.add_error('confirm_password', error)


class ProfileInfoChangeForm(forms.Form):

    first_name = forms.CharField(label="First Name",
                                 error_messages={'required': 'First Name Required.'},
                                 max_length=100,
                                 widget=forms.TextInput(attrs={
                                     'placeholder': 'First Name',
                                     'class': 'form-control'
                                 })
                                 )

    last_name = forms.CharField(label="Last Name",
                                error_messages={'required': 'Last Name Required.'},
                                max_length=100,
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'Last Name',
                                    'class': 'form-control'
                                })
                                )

    email = forms.CharField(label="Email",
                            required=False,
                            error_messages={'required': 'Email Required.'},
                            max_length=100,
                            widget=forms.EmailInput(attrs={
                                'placeholder': 'Email',
                                'class': 'form-control'
                            })
                            )

    profile_pic = forms.CharField(label="Choose Your Profile Pic",
                                  required=False,
                                  widget=forms.FileInput(attrs={
                                      'class': 'form-control'
                                  })
                                  )

    phone_number = forms.CharField(label="Phone number?",
                                   error_messages={'required': 'Phone number Required.'},
                                   max_length=100,
                                   widget=forms.NumberInput(attrs={
                                       'placeholder': 'Phone Number',
                                       'class': 'form-control'
                                   }))

    street = forms.CharField(label="Street?",
                             error_messages={'required': 'Street Required.'},
                             max_length=100,
                             widget=forms.TextInput(attrs={
                                 'placeholder': 'Street',
                                 'class': 'form-control'
                             }))

    postcode = forms.CharField(label="Postcode?",
                               error_messages={'required': 'Postcode Required.'},
                               max_length=100,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Postcode',
                                   'class': 'form-control'
                               }))

    city = forms.CharField(label="City?",
                           error_messages={'required': 'City Required.'},
                           max_length=100,
                           widget=forms.TextInput(attrs={
                               'placeholder': 'City',
                               'class': 'form-control'
                           }))
