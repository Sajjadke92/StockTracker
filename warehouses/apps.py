from django.apps import AppConfig


class WarehousesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField" # Specifies the default primary key field type for models in this app
    name = "warehouses"
