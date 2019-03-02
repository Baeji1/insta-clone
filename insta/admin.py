from django.contrib import admin
from .models import UserModel, Post, FollowModel, CommentModel,ActionModel

# Register your models here.
admin.site.register(UserModel)
admin.site.register(Post)
admin.site.register(FollowModel)
admin.site.register(CommentModel)
admin.site.register(ActionModel)