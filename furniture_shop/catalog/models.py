from django.db import models


class Customer(models.Model):
    """Модель покупателя (регистрация)"""
    username = models.CharField(max_length=100, verbose_name="Имя пользователя")
    email = models.EmailField(unique=True, verbose_name="Email")
    password = models.CharField(max_length=100, verbose_name="Пароль")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"


class Product(models.Model):
    """Модель товара (мебели) — хранится в PostgreSQL"""
    title = models.CharField(max_length=255, verbose_name='Название')
    category = models.CharField(max_length=100, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание')
    price = models.CharField(max_length=50, verbose_name='Цена')
    old_price = models.CharField(max_length=50, blank=True, null=True, verbose_name='Старая цена')
    image = models.URLField(max_length=500, verbose_name='Ссылка на изображение')
    color = models.CharField(max_length=100, verbose_name='Цвет')
    material = models.CharField(max_length=100, verbose_name='Материал')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0, verbose_name='Рейтинг')
    in_stock = models.BooleanField(default=True, verbose_name='В наличии')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class CartItem(models.Model):
    """Модель корзины — хранится в PostgreSQL"""
    user_email = models.EmailField(verbose_name="Email пользователя")
    product_id = models.IntegerField(verbose_name="ID товара")
    product_title = models.CharField(max_length=200, verbose_name="Название товара")
    product_price = models.CharField(max_length=50, verbose_name="Цена")
    quantity = models.IntegerField(default=1, verbose_name="Количество")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено")

    def __str__(self):
        return f"{self.product_title} x{self.quantity} ({self.user_email})"

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"


class Order(models.Model):
    """Модель заказа — хранится в PostgreSQL"""
    product_id = models.IntegerField(verbose_name="ID товара")
    product_title = models.CharField(max_length=200, verbose_name="Название товара")
    customer_name = models.CharField(max_length=100, verbose_name="Имя покупателя")
    customer_email = models.EmailField(verbose_name="Email")
    customer_phone = models.CharField(max_length=20, verbose_name="Телефон")
    quantity = models.IntegerField(default=1, verbose_name="Количество")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    delivery_method = models.CharField(max_length=20, default='delivery', verbose_name="Способ получения")
    delivery_address = models.TextField(blank=True, null=True, verbose_name="Адрес доставки")
    delivery_date = models.CharField(max_length=20, blank=True, null=True, verbose_name="Дата доставки")
    delivery_time = models.CharField(max_length=20, blank=True, null=True, verbose_name="Время доставки")
    pickup_point = models.CharField(max_length=200, blank=True, null=True, verbose_name="Адрес склада")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")

    def __str__(self):
        return f"Заказ №{self.id} - {self.customer_name} ({self.product_title})"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"