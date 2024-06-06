from .models import UserProfile

def user_credits(request):
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            return {'user_credits': user_profile.credits}
        except UserProfile.DoesNotExist:
            # Si el perfil no existe, devuelve créditos como 0
            return {'user_credits': 0}
    else:
        return {'user_credits': 0}
