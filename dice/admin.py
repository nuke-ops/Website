from datetime import datetime, timezone
from django.contrib import admin
from .models import Dice

threshold_date = datetime(2023, 10, 8)


class DiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "dice",
        "sides",
        "throws",
        "sum",
        "modifier",
        "formatted_date",
    )
    list_filter = ["date"]
    search_fields = ("id", "name", "date")

    actions = ["delete_records_before_date", "select_records_before_date"]

    def formatted_date(self, obj):
        return obj.date.strftime("%d-%m-%Y %H:%M:%S")

    formatted_date.admin_order_field = "date"
    formatted_date.short_description = "Formatted Date"

    def delete_records_before_date(self, request, queryset):
        records_to_delete = queryset.filter(date__lt=threshold_date)
        delete_count = records_to_delete.delete()[0]
        self.message_user(
            request,
            f"Successfully deleted {delete_count} records before {threshold_date}.",
        )

    delete_records_before_date.short_description = (
        "Delete records before a certain date"
    )

    def select_records_before_date(self, request, queryset):
        records_to_select = queryset.filter(date__lt=threshold_date)
        self.message_user(
            request,
            f"Successfully selected {len(records_to_select)} records before {threshold_date} | {records_to_select}.",
        )

    select_records_before_date.short_description = "Show records before a certain date"


admin.site.register(Dice, DiceAdmin)
