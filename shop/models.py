from django.contrib.postgres.indexes import  BTreeIndex
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from user.models import User
from PIL import Image
from django.db import models
from io import BytesIO
from django.core.files.base import ContentFile


def save_image(obj, height, weight):
    if obj:
        img = Image.open(obj)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        img = img.resize((height, weight), Image.Resampling.LANCZOS)
        # Сохраняем изменённое изображение в памяти
        buffer = BytesIO()
        img.save(buffer, format='JPEG')
        # Заменяем оригинальный файл новым
        obj.save(obj.name, ContentFile(buffer.getvalue()), save=False)
    return obj


class Category(MPTTModel):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    parent = TreeForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    image = models.ImageField(blank=True, null=True, upload_to="category/")
    svg_image = models.TextField(blank=True, null=True)

    def svg_display(self):
        return mark_safe(self.svg_image)

    class Meta:
        verbose_name_plural = 'Категории'
        indexes = [
            BTreeIndex(fields=["updated_at"], name="updated_at_idx"),
        ]

    def __str__(self) -> str:
        return self.name

    def get_category_path(self):
        """
        Возвращает путь от корневой категории до текущей в виде списка.
        """
        return self.get_ancestors(include_self=True)

    def get_absolute_url(self):
        # Проверяем, есть ли дочерние категории
        if self.children.exists():
            return reverse("shop:child_categories", kwargs={"id": self.id})
        else:
            return reverse("shop:products_list_by_category", kwargs={"category_slug": self.slug})

    def save(self, *args, **kwargs):
        save_image(self.image, 260, 200)
        super().save(*args, **kwargs)




class Product(models.Model):
    # product_type = models.ForeignKey(
    #     ProductType, related_name="products", on_delete=models.CASCADE
    # )
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField("Описание", blank=True, null=True)
    additional_info = models.TextField('Характеристики', blank=True, null=True)
    is_digital = models.BooleanField("Цифровые данные", default=False)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True, editable=False)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True, editable=False)
    is_active = models.BooleanField("Наличие", default=True)
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    stock_qty = models.IntegerField("Кол-во на складе", default=0)
    price = models.DecimalField("Цена", max_digits=6, decimal_places=2)
    main_image = models.ImageField("Фото", upload_to='products/main/', blank=True)

    vendor = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Продукты"
        ordering = ("slug",)

        indexes = [
            models.Index(
                fields=["category_id", "slug"],
            ),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        save_image(self.main_image, 200, 200)
        super().save(*args, **kwargs)


class ProductMedia(models.Model):
    product = models.ForeignKey(Product, related_name="media", on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="products", blank=True, null=True)
    alt = models.CharField(max_length=250, blank=True)

    class Meta:
        verbose_name_plural = 'Изображения'

    def save(self, *args, **kwargs):
        save_image(self.image, 600, 600)
        super().save(*args, **kwargs)


class Characteristic(models.Model):
    name = models.CharField("Название", max_length=100)
    description = models.TextField("Описание", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Тип продукта",
                                 related_name='characteristics')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Характеристики"


class CharacteristicValue(models.Model):
    value = models.CharField(" Значение атрибута", max_length=100)
    characteristic = models.ForeignKey(Characteristic, on_delete=models.CASCADE, verbose_name="Характеристика",
                                       related_name='cvalue')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт", related_name='cvalue')

    def __str__(self):
        return f"{self.characteristic}:{self.value}"


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт", related_name="reviews")
    review = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
