from asgiref.sync import sync_to_async
from botapp.models import BotUser
from product.models import SoftSlideMirror, SoftSlideElement

class Database:

    @staticmethod
    @sync_to_async
    def get_or_create_user(user_id: int, username: str = None, full_name: str = None, is_bot: bool = False, user_type: str = 'customer'):
        """
        Get or create a user in the database.
        """
        user, created = BotUser.objects.get_or_create(
            user_id=user_id,
            defaults={
                'username': username,
                'full_name': full_name,
                'is_bot': is_bot,
                'user_type': user_type
            }
        )
        return {
            'user_id': user.user_id,
            'username': user.username,
            'full_name': user.full_name,
            'is_bot': user.is_bot,
            'is_active': user.is_active,
            'is_admin': user.is_admin,
            'user_type': user.user_type,
            'created_at': user.created_at,
            'updated_at': user.updated_at,
            'created': created
        }
    

    @staticmethod
    @sync_to_async
    def get_softslide_mirrors_name():
        """
        Get all soft slide mirrors from the database.
        """
        return SoftSlideMirror.objects.all().values_list('name', flat=True)


    @staticmethod
    @sync_to_async
    def get_softslide_mirror_by_name(name: str):
        """
        Get a soft slide mirror by its name.
        """
        return SoftSlideMirror.objects.filter(name=name).first()