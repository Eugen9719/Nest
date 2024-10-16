from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile


# Декоратор @receiver связывает сигнал post_save с функцией create_user_profile.
# Это означает, что каждый раз после сохранения модели User будет вызвана эта функция.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Создает профиль пользователя после создания нового пользователя.

    Аргументы:
    - sender: модель, отправившая сигнал (в данном случае модель User).
    - instance: экземпляр модели User, который был сохранен.
    - created: булево значение, указывающее, был ли создан новый экземпляр (True) или обновлен существующий (False).
    - **kwargs: дополнительные аргументы.
    """
    if created:
        # Если был создан новый пользователь, создаем для него связанный профиль.
        Profile.objects.create(user=instance)


# Второй декоратор @receiver связывает тот же сигнал post_save с функцией save_user_profile. Эта функция вызывается
# каждый раз после сохранения модели User, независимо от того, создан ли новый пользователь или обновлен существующий.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """
    Сохраняет профиль пользователя после сохранения пользователя.

    Аргументы:
    - sender: модель, отправившая сигнал (в данном случае модель User).
    - instance: экземпляр модели User, который был сохранен.
    - **kwargs: дополнительные аргументы.
    """
    # Сохраняем связанный профиль пользователя. Это полезно, если профиль уже существует и его данные изменились.
    instance.profile.save()
