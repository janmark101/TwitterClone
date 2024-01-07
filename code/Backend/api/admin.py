from django.contrib import admin
from .models import  Comment,Tweet,Like
# Register your models here.

class TweetAdmin(admin.ModelAdmin):
    filter_horizontal = ('retweets',)

admin.site.register(Comment)
admin.site.register(Tweet,TweetAdmin)
admin.site.register(Like)