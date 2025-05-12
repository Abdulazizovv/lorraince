from django.db import models


class BotUser(models.Model):
    """
    Model representing a user of the bot.
    """
    user_id = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    is_bot = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    type_choices = (
        ('customer', 'Customer'),
        ('seller', 'Seller'),
        ('master', 'Master'),
    )
    user_type = models.CharField(max_length=50, choices=type_choices, default='customer')


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username or self.user_id
    