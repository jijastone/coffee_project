from django.contrib import admin

from .models import UserProfile, Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    readonly_fields = ('document_type',)


admin.site.register(UserProfile)