from django import forms


class CheckoutForm(forms.Form):

    choose_country = [
        ('Germany', 'Germany')
    ]

    choose_payment = [
        ('Cash On Delivery', 'Cash on Delivery'),
        ('Paypal', 'Paypal')
    ]

    first_name = forms.CharField(label="First Name",
                                 error_messages={'required': 'First Name Required.'},
                                 max_length=100,
                                 widget=forms.TextInput(attrs={
                                     'placeholder': 'First Name',
                                     'class': 'form-control name-format'
                                 }))

    last_name = forms.CharField(label="Last Name",
                                error_messages={'required': 'Last Name Required.'},
                                max_length=100,
                                widget=forms.TextInput(attrs={
                                     'placeholder': 'Last Name',
                                     'class': 'form-control name-format'
                                 }))

    email = forms.EmailField(label="Email?",
                             error_messages={'required': 'Valid Email Required.'},
                             max_length=100,
                             help_text='We will send you a email to this email.',
                             widget=forms.EmailInput(attrs={
                                 'placeholder': 'Email',
                                 'class': 'form-control name-format'
                             }))

    phone_number = forms.CharField(label="Phone number?",
                                   error_messages={'required': 'Phone number Required.'},
                                   max_length=100,
                                   widget=forms.NumberInput(attrs={
                                       'placeholder': 'Phone Number',
                                       'class': 'form-control name-format'
                                   }))

    country = forms.CharField(label='Country / Region',
                              widget=forms.Select(
                                  choices=choose_country,
                                  attrs={
                                      'class': 'selectcountry'
                                         }))

    street = forms.CharField(label="Street",
                             error_messages={'required': 'Street Required.'},
                             max_length=100,
                             widget=forms.TextInput(attrs={
                                 'placeholder': 'Street',
                                 'class': 'form-control name-format'
                             }))

    optional = forms.CharField(label="Optional",
                               required=False,
                               max_length=100,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Optional',
                                   'class': 'form-control name-format'
                               }))

    city = forms.CharField(label="City",
                           error_messages={'required': 'City Required.'},
                           max_length=100,
                           widget=forms.TextInput(attrs={
                               'placeholder': 'City',
                               'class': 'form-control name-format'
                           }))

    post_code = forms.CharField(label="Postcode",
                                error_messages={'required': 'Postcode Required.'},
                                max_length=100,
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'Postcode',
                                    'class': 'form-control name-format'
                                }))

    different_shipping_address = forms.BooleanField(required=False)

    different_first_name = forms.CharField(label="First Name",
                                           required=False,
                                           error_messages={'required': 'First Name Required.'},
                                           max_length=100,
                                           widget=forms.TextInput(attrs={
                                               'placeholder': 'First Name',
                                               'class': 'form-control name-format'
                                           }))

    different_last_name = forms.CharField(label="Last Name",
                                          required=False,
                                          error_messages={'required': 'Last Name Required.'},
                                          max_length=100,
                                          widget=forms.TextInput(attrs={
                                              'placeholder': 'Last Name',
                                              'class': 'form-control name-format'
                                          }))

    different_email = forms.EmailField(label="Email?",
                                       required=False,
                                       error_messages={'required': 'Valid Email Required.'},
                                       max_length=100,
                                       help_text='We will send you a email to this email.',
                                       widget=forms.EmailInput(attrs={
                                           'placeholder': 'Email',
                                           'class': 'form-control name-format'
                                       }))

    different_phone_number = forms.CharField(label="Phone number?",
                                             required=False,
                                             error_messages={'required': 'Phone number Required.'},
                                             max_length=100,
                                             widget=forms.NumberInput(attrs={
                                                 'placeholder': 'Phone Number',
                                                 'class': 'form-control name-format'
                                             }))

    different_country = forms.CharField(label='Country / Region',
                                        required=False,
                                        widget=forms.Select(
                                            choices=choose_country,
                                            attrs={
                                                'class': 'selectcountry'
                                            }))

    different_street = forms.CharField(label="Street",
                                       required=False,
                                       error_messages={'required': 'Street Required.'},
                                       max_length=100,
                                       widget=forms.TextInput(attrs={
                                           'placeholder': 'Street',
                                           'class': 'form-control name-format'
                                       }))

    different_optional = forms.CharField(label="Optional",
                                         required=False,
                                         max_length=100,
                                         widget=forms.TextInput(attrs={
                                             'placeholder': 'Optional',
                                             'class': 'form-control name-format'
                                         }))

    different_city = forms.CharField(label="City",
                                     required=False,
                                     error_messages={'required': 'City Required.'},
                                     max_length=100,
                                     widget=forms.TextInput(attrs={
                                         'placeholder': 'City',
                                         'class': 'form-control name-format'
                                     }))

    different_post_code = forms.CharField(label="Postcode",
                                          required=False,
                                          error_messages={'required': 'Postcode Required.'},
                                          max_length=100,
                                          widget=forms.TextInput(attrs={
                                              'placeholder': 'Postcode',
                                              'class': 'form-control name-format'
                                          }))

    comment_on_the_order = forms.CharField(required=False,
                                           widget=forms.Textarea(attrs={
                                               'placeholder': 'Comments on the order (optional)',
                                               'class': 'form-control',
                                               'cols': '20',
                                               'rows': '5'
                                           }))

    payment = forms.ChoiceField(choices=choose_payment,
                                widget=forms.RadioSelect(attrs={
                                    'checked': True
                                }))

    agree = forms.BooleanField(
        error_messages={'required': 'You Have to agree with us.'},
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }))
