from django.shortcuts import render, redirect
from .forms import ContactForm

def index(request):
    title = 'Интернет-магазин мебели "Уютный дом"'
    subtitle = 'Мебель для вашего комфорта'
    categories = ['Гостиная', 'Спальня', 'Кухня', 'Детская', 'Офис', 'Прихожая']
    return render(request, 'homepage/index.html', {
        'title': title,
        'subtitle': subtitle,
        'categories': categories,
    })

def contacts(request):
    """
    Страница контактов с формой обратной связи.
    При успешной отправке — редирект на главную, данные в консоль.
    """
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Вывод данных в консоль (по заданию 4.9)
            print('=' * 50)
            print('НОВОЕ СООБЩЕНИЕ ОБРАТНОЙ СВЯЗИ:')
            print(f"Имя: {form.cleaned_data['name']}")
            print(f"Email: {form.cleaned_data['email']}")
            print(f"Сообщение: {form.cleaned_data['message']}")
            print('=' * 50)
            # Перенаправление на главную страницу
            return redirect('homepage:index')
    
    return render(request, 'contacts.html', {
        'title': 'Контакты',
        'form': form,
    })