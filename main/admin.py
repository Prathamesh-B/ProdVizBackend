from django.contrib import admin
from .models import ProductionLine, Tag, Log, Alert

admin.site.register(ProductionLine)
admin.site.register(Tag)
admin.site.register(Log)
admin.site.register(Alert)
