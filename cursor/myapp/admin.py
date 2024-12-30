from django.contrib import admin

# Register your models here.
from .models import Item
from django.shortcuts import redirect, render
from django.urls import path
from .views import fetch_twilio_numbers



@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["name","description","created_at"]
    actions = ['fetch_and_compare_twilio_numbers']
    change_list_template = "admin/myapp/item/change_list.html"


    def fetch_and_compare_twilio_numbers(self, request, queryset):
        # Redirect to a custom view
        return redirect('admin:fetch_twilio_numbers')

    fetch_and_compare_twilio_numbers.short_description = "Fetch and compare Twilio numbers"

    def get_urls(self):
            urls = super().get_urls()
            custom_urls = [
                path('fetch_twilio_numbers/', self.admin_site.admin_view(fetch_twilio_numbers), name='fetch_twilio_numbers'),
            ]
            return custom_urls + urls