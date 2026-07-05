from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from .models import Customer, Product, Order, CartItem
import re
import random
import string


def validate_phone(phone):
    pattern = r'^[\d\s\+\-\(\)]{7,15}$'
    return re.match(pattern, phone) is not None


# ========== ГЛАВНАЯ ==========
def home(request):
    return render(request, 'index.html', {'title': 'Главная'})


# ========== КАТАЛОГ ==========
def catalog(request):
    products = Product.objects.filter(in_stock=True)
    return render(request, 'catalog.html', {'products': products, 'title': 'Каталог'})


# ========== КАРТОЧКА ТОВАРА ==========
def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        product = None
    return render(request, 'product.html', {'product': product})


# ========== КОНТАКТЫ ==========
def contacts(request):
    return render(request, 'contacts.html', {'title': 'Контакты'})


# ========== ВХОД / РЕГИСТРАЦИЯ ==========
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        errors = []

        if len(username) < 2:
            errors.append('Имя должно содержать минимум 2 символа')
        if len(username) > 50:
            errors.append('Имя слишком длинное (максимум 50 символов)')

        try:
            validate_email(email)
        except ValidationError:
            errors.append('Введите корректный email адрес')

        if len(password) < 4:
            errors.append('Пароль должен содержать минимум 4 символа')

        if errors:
            for error in errors:
                messages.error(request, f'❌ {error}')
            return render(request, 'login.html')

        customer = Customer.objects.filter(email=email).first()
        if customer:
            request.session['user_email'] = email
            request.session['user_name'] = customer.username
            messages.success(request, f'✅ С возвращением, {customer.username}!')
        else:
            Customer.objects.create(username=username, email=email, password=password)
            request.session['user_email'] = email
            request.session['user_name'] = username
            messages.success(request, f'🎉 {username}, регистрация успешна!')

        return redirect('home')

    return render(request, 'login.html')


# ========== ВЫХОД ==========
def logout_view(request):
    request.session.flush()
    messages.success(request, '👋 Вы вышли из аккаунта')
    return redirect('home')


# ========== ДОБАВЛЕНИЕ В КОРЗИНУ ==========
def add_to_cart(request, product_id):
    if 'user_email' not in request.session:
        messages.error(request, '❌ Сначала войдите в аккаунт!')
        return redirect('login')

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, '❌ Товар не найден')
        return redirect('catalog')

    existing = CartItem.objects.filter(
        user_email=request.session['user_email'],
        product_id=product_id
    ).first()

    if existing:
        existing.quantity += 1
        existing.save()
        messages.success(request, f'✅ Количество "{product.title}" увеличено до {existing.quantity} шт.')
    else:
        CartItem.objects.create(
            user_email=request.session['user_email'],
            product_id=product.id,
            product_title=product.title,
            product_price=product.price,
            quantity=1
        )
        messages.success(request, f'✅ "{product.title}" добавлен в корзину!')

    return redirect('cart')


# ========== УДАЛЕНИЕ ИЗ КОРЗИНЫ ==========
def remove_from_cart(request, item_id):
    item = CartItem.objects.filter(id=item_id).first()
    if item:
        title = item.product_title
        item.delete()
        messages.success(request, f'🗑️ "{title}" удалён из корзины')
    return redirect('cart')


# ========== КОРЗИНА ==========
def cart_view(request):
    if 'user_email' not in request.session:
        messages.error(request, '❌ Сначала войдите в аккаунт!')
        return redirect('login')

    cart_items = CartItem.objects.filter(user_email=request.session['user_email'])
    return render(request, 'cart.html', {'cart_items': cart_items})


# ========== ОФОРМЛЕНИЕ ЗАКАЗА ==========
def checkout(request):
    if 'user_email' not in request.session:
        messages.error(request, '❌ Сначала войдите в аккаунт!')
        return redirect('login')

    if request.method != 'POST':
        return redirect('cart')

    cart_items = CartItem.objects.filter(user_email=request.session['user_email'])

    if not cart_items:
        messages.error(request, '❌ Корзина пуста!')
        return redirect('cart')

    phone = request.POST.get('phone', '').strip()
    delivery_method = request.POST.get('delivery_method', 'delivery')
    address = request.POST.get('address', '').strip()
    delivery_date = request.POST.get('delivery_date', '').strip()
    delivery_time = request.POST.get('delivery_time', '').strip()
    pickup_point = request.POST.get('pickup_point', '').strip()

    errors = []

    if not phone:
        errors.append('Введите номер телефона')
    elif not validate_phone(phone):
        errors.append('Некорректный номер телефона')

    if delivery_method not in ['delivery', 'pickup']:
        errors.append('Выберите способ получения')

    if delivery_method == 'delivery':
        if not address:
            errors.append('Введите адрес доставки')
        if not delivery_date:
            errors.append('Выберите дату доставки')
        if not delivery_time:
            errors.append('Выберите время доставки')

    if delivery_method == 'pickup':
        if not pickup_point:
            errors.append('Выберите склад для самовывоза')

    if errors:
        for error in errors:
            messages.error(request, f'❌ {error}')
        return redirect('cart')

    for item in cart_items:
        Order.objects.create(
            product_id=item.product_id,
            product_title=item.product_title,
            customer_name=request.session.get('user_name', ''),
            customer_email=request.session['user_email'],
            customer_phone=phone,
            quantity=item.quantity,
            delivery_method=delivery_method,
            delivery_address=address if delivery_method == 'delivery' else '',
            delivery_date=delivery_date if delivery_method == 'delivery' else '',
            delivery_time=delivery_time if delivery_method == 'delivery' else '',
            pickup_point=pickup_point if delivery_method == 'pickup' else '',
        )

    cart_items.delete()
    messages.success(request, '🎉 Заказ успешно оформлен!')
    return redirect('my_orders')


# ========== ЗАКАЗЫ ==========
def my_orders(request):
    if 'user_email' not in request.session:
        messages.error(request, '❌ Сначала войдите в аккаунт!')
        return redirect('login')

    orders = Order.objects.filter(
        customer_email=request.session['user_email']
    ).order_by('-created_at')

    return render(request, 'orders.html', {
        'orders': orders,
        'title': 'Мои заказы'
    })


# ========== ВОССТАНОВЛЕНИЕ ПАРОЛЯ ==========
def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        customer = Customer.objects.filter(email=email).first()
        
        if customer:
            # Генерируем новый пароль
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            
            # Сохраняем новый пароль в БД
            customer.password = new_password
            customer.save()
            
            # Отправляем письмо (сохраняется в папку sent_emails)
            send_mail(
                'Восстановление пароля — Уютный дом',
                f'Здравствуйте, {customer.username}!\n\n'
                f'Ваш новый пароль: {new_password}\n\n'
                f'Вы можете войти на сайт: http://127.0.0.1:8000/login/\n\n'
                f'С уважением, магазин мебели "Уютный дом"',
                'noreply@uyutny-dom.ru',
                [email],
                fail_silently=False,
            )
            
            messages.success(request, f'✅ Новый пароль отправлен на {email}')
            messages.info(request, '📧 Письмо сохранено в папке sent_emails')
        else:
            messages.error(request, '❌ Пользователь с таким email не найден')
        
        return redirect('login')
    
    return render(request, 'password_reset.html')