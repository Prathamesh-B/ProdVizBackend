from django.contrib import admin
from .models import (
    AuthRole, AuthUser, Plant, Block, Line, Machine, 
    SensorTagType, SensorTag, DaqLog, Alert, Incident, 
    IncidentTransaction
)

admin.site.register(AuthRole)
admin.site.register(AuthUser)
admin.site.register(Plant)
admin.site.register(Block)
admin.site.register(Line)
admin.site.register(Machine)
admin.site.register(SensorTagType)
admin.site.register(SensorTag)
admin.site.register(DaqLog)
admin.site.register(Alert)
admin.site.register(Incident)
admin.site.register(IncidentTransaction)