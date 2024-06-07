from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import UserProfile
from allauth.socialaccount.signals import social_account_added, social_account_updated, pre_social_login

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()

@receiver(social_account_added)
def populate_profile_image(request, sociallogin, **kwargs):
    user = sociallogin.user
    picture_url = sociallogin.account.extra_data.get('picture')
    
    if picture_url:
        UserProfile.objects.update_or_create(user=user, defaults={'profile_image': picture_url})

@receiver(social_account_added)
def social_account_added_receiver(request, sociallogin, **kwargs):
    user = sociallogin.user
    picture_url = sociallogin.account.extra_data.get('picture')

    if picture_url:
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.profile_image = picture_url
        user_profile.save()


def social_account_updated_receiver(request, sociallogin, **kwargs):
    user = sociallogin.user
    picture_url = sociallogin.account.extra_data.get('picture')

    if picture_url:
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.profile_image = picture_url
        user_profile.save()


@receiver(pre_social_login)
def update_profile_image_on_login(sender, request, sociallogin, **kwargs):
    user = sociallogin.user
    picture_url = sociallogin.account.extra_data.get('picture')

    if picture_url:
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.profile_image = picture_url
        user_profile.save()
