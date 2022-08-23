from django import forms


class ContactForm(forms.Form):

    name = forms.CharField(error_messages = {
        'required' : 'Please enter your Full Name.'
        },
        widget = forms.TextInput( attrs = {
            'placeholder' : 'Full Name',
            'autocomplete': 'off',
            'class' : 'form-control'
        })
    )

    email = forms.EmailField(error_messages={
        'required' : 'Please use A Vaild Email.'
        },
        widget = forms.EmailInput( attrs = {
            'placeholder' : 'Email',
            'autocomplete': 'off',
            'class' : 'form-control'
        })
    )

    subject = forms.CharField(error_messages = {
        'required' : 'Please enter your Subject.'
        },
        widget = forms.TextInput( attrs = {
            'placeholder' : 'Subject',
            'autocomplete': 'off',
            'class' : 'form-control'
        })
    )
    

    message = forms.CharField(error_messages = {
        'required' : 'Your Message Is Important For Us.'
        },
        widget = forms.Textarea( attrs = {
            'class' : 'form-control',
            'autocomplete': 'off',
            'style': 'height: 150px',
            'placeholder' : 'How can we help you?',
            'rows' : 6
        })
    )
