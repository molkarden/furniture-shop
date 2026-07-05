from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    """
    Форма заказа товара. Связана с моделью Order.
    """
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'customer_phone', 'quantity', 'comment']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя'
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@mail.ru'
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 123-45-67'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'value': 1
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Дополнительные пожелания (необязательно)'
            }),
        }
        labels = {
            'customer_name': 'Ваше имя',
            'customer_email': 'Email',
            'customer_phone': 'Телефон',
            'quantity': 'Количество',
            'comment': 'Комментарий',
        }