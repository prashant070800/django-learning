from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Call, Sim

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    search_fields = ("email",)
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active"),
        }),
    )


@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ("fron_number", "to_number", "sid")
    search_fields = ("fron_number", "to_number", "sid")
from django.contrib import admin
from django.db.models import Count, Q, OuterRef, Subquery, Value, IntegerField
from django.db.models.functions import Coalesce
from .models import Call, Sim  # Import your models
from django.contrib import admin
from django.db.models import Count, Q, OuterRef, Subquery, Value, IntegerField
from django.db.models.functions import Coalesce
from .models import Call, Sim
@admin.register(Sim)
class SimAdmin(admin.ModelAdmin):
    list_display = ("user", "uid", "call_count")
    search_fields = ("user__username", "uid")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                call_count=Coalesce(
                    Subquery(
                        Call.objects.filter(
                            Q(fron_number=OuterRef("uid")) | Q(to_number=OuterRef("uid"))
                        )
                        # .values('fron_number') # Count distinct calls
                        .annotate(total_count=Count('id', distinct=True))
                        .values('total_count'),
                        output_field=IntegerField()
                    ),
                    Value(0),
                    output_field=IntegerField(),
                )
            )
        )

    def call_count(self, obj):
        count = Call.objects.filter(Q(fron_number=obj.uid) | Q(to_number=obj.uid)).annotate(total_count=Count("id", distinct=True)).values()
        print(f"UID: {obj.uid}, Count: {count} call_count: {obj.call_count}")
        return obj.call_count

    call_count.short_description = "Call Count"
    call_count.admin_order_field = "call_count"
