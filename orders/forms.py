from django import forms

from orders.models import Order


class OrderCreateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-group col-lg-6', 'placeholder': 'Введите имя '}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-group col-lg-6', 'placeholder': 'Введите фамилию'}))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-group col-lg-6', 'placeholder': 'Введите адрес '}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-group col-lg-6', 'placeholder': 'Введите адрес электронной почты '}))
    postal_code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-group col-lg-6', 'placeholder': ''}))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-group col-lg-6', 'placeholder': 'Введите город '}))

    comment = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-group mb-30', 'placeholder': 'Комментарий '}), required=False)

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'address', 'email', 'postal_code', 'city', 'comment')
