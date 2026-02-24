from django import forms


class ContactForm(forms.Form):
    ad_soyad = forms.CharField(
        max_length=100,
        label='Ad Soyad',
        widget=forms.TextInput(attrs={'placeholder': 'Adınız ve soyadınız'}),
    )
    email = forms.EmailField(
        label='E-posta',
        widget=forms.EmailInput(attrs={'placeholder': 'ornek@mail.com'}),
    )
    mesaj = forms.CharField(
        label='Mesaj',
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Mesajınızı buraya yazın...',
        }),
    )
