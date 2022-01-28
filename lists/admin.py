from django.contrib import admin

from .models import List, Bullet

class BulletsInLine(admin.StackedInline):
    model = Bullet

class ListAdmin(admin.ModelAdmin):
    inlines=[
        BulletsInLine,
    ]

admin.site.register(List, ListAdmin)
admin.site.register(Bullet)
