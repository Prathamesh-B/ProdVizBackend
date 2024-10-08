from rest_framework import serializers
from .models import (
    AuthRole, AuthUser, Plant, Block, Line, Machine, 
    SensorTagType, SensorTag, DaqLog, Alert, Incident, 
    IncidentTransaction
)

class AuthRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthRole
        fields = '__all__'

class AuthUserSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField()

    class Meta:
        model = AuthUser
        fields = '__all__'

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'

class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = '__all__'

class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line
        fields = '__all__'

class MachineSerializer(serializers.ModelSerializer):
    line = LineSerializer(read_only=True)
    line_id = serializers.PrimaryKeyRelatedField(queryset=Line.objects.all(), source='line', write_only=True)

    class Meta:
        model = Machine
        fields = '__all__'

class SensorTagTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorTagType
        fields = '__all__'

class SensorTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorTag
        fields = '__all__'

class DaqLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DaqLog
        fields = '__all__'

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'

class IncidentSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.name', read_only=True)
    line_name = serializers.CharField(source='line.name', read_only=True)
    tag_name = serializers.CharField(source='tag.name', read_only=True)

    class Meta:
        model = Incident
        fields = '__all__'

class IncidentTransactionSerializer(serializers.ModelSerializer):
    issued_by_name = serializers.CharField(source='issued_by.name', read_only=True)

    class Meta:
        model = IncidentTransaction
        fields = '__all__'