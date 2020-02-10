from django.contrib import admin
from .models import Images,GroupImage,Group
# Register your models here.


admin.site.register(Group)
admin.site.register(Images)
admin.site.register(GroupImage)