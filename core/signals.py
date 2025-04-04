from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from core.models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
            phone_number='09120000000',  # مقدار پیش‌فرض
            national_code='0000000000',  # مقدار پیش‌فرض
            address='نامشخص'  # مقدار پیش‌فرض
        )