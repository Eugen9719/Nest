from django.db import models
from django.urls import reverse

from user.models import User


class Product(models.Model):
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField("Описание", blank=True, null=True)
    additional_info = models.TextField('Характеристики', blank=True, null=True)
    is_digital = models.BooleanField("Цифровые данные", default=False)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True, editable=False)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True, editable=False)
    is_active = models.BooleanField("Наличие", default=True)

    stock_qty = models.IntegerField("Кол-во на складе", default=0)
    price = models.DecimalField("Цена", max_digits=6, decimal_places=2)
    main_image = models.ImageField("Фото", upload_to='products/main/', blank=True)

    vendor = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Продукты"

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])
