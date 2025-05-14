from django.contrib import admin
from product.models import SoftSlideDye, SoftSlide, SoftSlideElement, SoftSlideMirror
# Register your models he

admin.site.register(SoftSlide)
admin.site.register(SoftSlideElement)
admin.site.register(SoftSlideMirror)
admin.site.register(SoftSlideDye)