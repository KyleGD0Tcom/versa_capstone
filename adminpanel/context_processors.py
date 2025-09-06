from .models import UserSettings

def user_settings_processor(request):
    """Context processor to make user settings available globally"""
    if request.user.is_authenticated:
        try:
            user_settings = UserSettings.objects.get(user=request.user)
            return {
                'user_settings': user_settings
            }
        except UserSettings.DoesNotExist:
            # Return default settings if none exist
            return {
                'user_settings': {
                    'timezone': 'UTC+08:00',
                    'date_format': 'MM/DD/YYYY'
                }
            }
    return {
        'user_settings': {
            'timezone': 'UTC+08:00',
            'date_format': 'MM/DD/YYYY'
        }
    }
