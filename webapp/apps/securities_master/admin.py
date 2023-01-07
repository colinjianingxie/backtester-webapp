from django.contrib import admin
from securities_master.models import Symbol, Exchange, DataVendor, DailyPrice


class SymbolAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "ticker",
        "exchange",
        "instrument",
        "name",
        "sector",
        "currency",
        "created_date",
        "last_updated_date",
    )  # What to display as columns in
    search_fields = ("id","ticker")
    readonly_fields = (
        "id",
        "ticker",
        "exchange",
        "instrument",
        "name",
        "sector",
        "currency",
        "created_date",
        "last_updated_date",
    )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class DailyPriceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "data_vendor",
        "symbol",
        "price_date",
        "created_date",
        "last_updated_date",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "adj_close_price",
        "volume",
    )  # What to display as columns in
    search_fields = ("id","symbol","data_vendor","price_date",)
    readonly_fields = (
        "id",
        "data_vendor",
        "symbol",
        "price_date",
        "created_date",
        "last_updated_date",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "adj_close_price",
        "volume",
    )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class DataVendorAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "website_url",
        "support_email",
        "created_date",
        "last_updated_date",
    )  # What to display as columns in
    search_fields = ("id",)
    readonly_fields = (
        "id",
        "name",
        "website_url",
        "support_email",
        "created_date",
        "last_updated_date",
    )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class ExchangeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "abbrev",
        "name",
        "city",
        "country",
        "currency",
        "timezone_offset",
        "created_date",
        "last_updated_date",
    )  # What to display as columns in
    search_fields = ("id",)
    readonly_fields = (
        "id",
        "abbrev",
        "name",
        "city",
        "country",
        "currency",
        "timezone_offset",
        "created_date",
        "last_updated_date",
    )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Symbol, SymbolAdmin)
admin.site.register(DailyPrice, DailyPriceAdmin)
admin.site.register(DataVendor, DataVendorAdmin)
