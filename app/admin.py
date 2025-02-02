from django.contrib import admin
from .models import Postform,Profile,Comments

# Register your models here.



admin.site.register(Postform)
admin.site.register(Profile)
admin.site.register(Comments)

# >>> from django.contrib.auth.models import Group, Permission, User
# >>> from django.contrib.auth.contenttypes.models import ContentType
# mod, created = Group.objects.get_or_create(name = 'mod')
#  from app.models import Postform

# ct = ContentType.objects.get_for_model(model=Postform)
#  perms = Permission.objects.filter(content_type = ct)
# >> mod.permissions.add(*perms)
#  user = User.objects.filter(username = 'muchi') 
# mod.user_set.add(user.first())
 
