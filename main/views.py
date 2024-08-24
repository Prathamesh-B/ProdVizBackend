from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Line, SensorTag, DaqLog, Alert, Plant, Block, Machine
from .serializers import (
    LineSerializer, SensorTagSerializer, DaqLogSerializer, AlertSerializer,
    PlantSerializer, BlockSerializer, MachineSerializer
)
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.db.models import Sum
import random

class DaqLogView(APIView):
    def get(self, request):
        line_id = request.query_params.get('LineId')
        machine_id = request.query_params.get('MachineId')
        tag_id = request.query_params.get('TagId')
        start_date = request.query_params.get('StartDate')
        end_date = request.query_params.get('EndDate')

        if not all([line_id, machine_id, tag_id, start_date, end_date]):
            return Response(
                {"error": "LineId, MachineId, TagId, StartDate, and EndDate are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            start_date = parse_datetime(start_date)
            end_date = parse_datetime(end_date)
            if start_date is None or end_date is None:
                raise ValueError
        except ValueError:
            return Response({"error": "Invalid date format."}, status=status.HTTP_400_BAD_REQUEST)

        if start_date >= end_date:
            return Response({"error": "StartDate must be before EndDate."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = DaqLog.objects.filter(
            tag__machine__line_id=line_id,
            tag__machine_id=machine_id,
            tag_id=tag_id,
            timestamp__range=(start_date, end_date)
        )

        serializer = DaqLogSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#remove in the future
class MachinePerformanceView(APIView):
    def get(self, request):
        start_date = request.query_params.get('StartDate')
        end_date = request.query_params.get('EndDate')

        if not start_date or not end_date:
            return Response(
                {"error": "StartDate and EndDate are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            start_date = parse_datetime(start_date)
            end_date = parse_datetime(end_date)
            if start_date is None or end_date is None:
                raise ValueError
        except ValueError:
            return Response({"error": "Invalid date format."}, status=status.HTTP_400_BAD_REQUEST)

        if start_date >= end_date:
            return Response({"error": "StartDate must be before EndDate."}, status=status.HTTP_400_BAD_REQUEST)

        lines = Line.objects.all()
        performance_data = []

        for line in lines:
            logs = DaqLog.objects.filter(
                tag__machine__line=line,
                timestamp__range=(start_date, end_date)
            )

            production_logs = logs.filter(tag__name__icontains='Production')
            production = production_logs.aggregate(total_production=Sum('value'))['total_production'] or 0

            downtime_logs = logs.filter(tag__name__icontains='Downtime')
            downtime = downtime_logs.aggregate(total_downtime=Sum('value'))['total_downtime'] or 0

            performance_data.append({
                "line_id": line.id,
                "line_name": line.name,
                "production": production,
                "downtime": downtime
            })

        return Response(performance_data, status=status.HTTP_200_OK)

class LineViewSet(viewsets.ModelViewSet):
    queryset = Line.objects.all()
    serializer_class = LineSerializer

class SensorTagViewSet(viewsets.ModelViewSet):
    queryset = SensorTag.objects.all()
    serializer_class = SensorTagSerializer

class DaqLogViewSet(viewsets.ModelViewSet):
    queryset = DaqLog.objects.all()
    serializer_class = DaqLogSerializer

class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

class BlockViewSet(viewsets.ModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer

class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

class AlertView(APIView):
    def get(self, request):
        line_id = request.query_params.get('Line', None)
        start_date = request.query_params.get('StartDate')
        end_date = request.query_params.get('EndDate')

        if start_date and end_date:
            start_date = parse_datetime(start_date)
            end_date = parse_datetime(end_date)
            alerts = Alert.objects.filter(timestamp__range=[start_date, end_date])
            if line_id:
                alerts = alerts.filter(line=line_id)
        else:
            alerts = Alert.objects.all().order_by('-timestamp')[:25]

        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AlertSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            alert = Alert.objects.get(pk=pk)
        except Alert.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AlertSerializer(alert, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            alert = Alert.objects.get(pk=pk)
        except Alert.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AlertSerializer(alert, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            alert = Alert.objects.get(pk=pk)
        except Alert.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        alert.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ControlPanelDataView(APIView):
    def post(self, request):
        lines = Line.objects.filter(status='active')
        sensor_tags = SensorTag.objects.all()
        
        logs = []
        timestamp = timezone.localtime(timezone.now())
        
        for line in lines:
            for machine in Machine.objects.filter(line=line):
                for tag in sensor_tags.filter(machine=machine):
                    if tag.name == 'Watts Consumed':
                        value = request.data.get('Vry', 0)
                    elif tag.name == 'Voltage Phase R-Y':
                        value = request.data.get('Vry', 0)
                    elif tag.name == 'Voltage Phase Y-B':
                        value = request.data.get('Vyb', 0)
                    elif tag.name == 'Voltage Phase B-R':
                        value = request.data.get('Vbr', 0)
                    elif tag.name == 'Current Phase R':
                        value = request.data.get('Cr', 0)
                    elif tag.name == 'Current Phase Y':
                        value = request.data.get('Cy', 0)
                    elif tag.name == 'Current Phase B':
                        value = request.data.get('Cb', 0)
                    elif tag.name == 'Frequency':
                        value = request.data.get('Freq', 0)
                    elif tag.name == 'Temperature':
                        value = request.data.get('Temp', 0)
                    else:
                        value = random.uniform(tag.min_val, tag.max_val)

                    value = max(min(value, tag.max_val), tag.min_val)

                    log = DaqLog(
                        timestamp=timestamp,
                        tag=tag,
                        value=value
                    )
                    logs.append(log)

        DaqLog.objects.bulk_create(logs)

        return Response({"message": "Data logged successfully"}, status=status.HTTP_201_CREATED)

class ProductionLineDetailView(APIView):
    def get(self, request):
        lines = Line.objects.all()
        result = []

        for line in lines:
            line_data = LineSerializer(line).data
            machines = Machine.objects.filter(line=line)
            line_data['machines'] = []

            for machine in machines:
                machine_data = MachineSerializer(machine).data
                tags = SensorTag.objects.filter(machine=machine)
                machine_data['tags'] = SensorTagSerializer(tags, many=True).data
                line_data['machines'].append(machine_data)

            result.append(line_data)

        return Response(result, status=status.HTTP_200_OK)

class ProductionMetricsView(APIView):
    def get(self, request):
        line_id = request.query_params.get('line_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not all([line_id, start_date, end_date]):
            return Response(
                {"error": "line_id, start_date, and end_date are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            start_date = parse_datetime(start_date)
            end_date = parse_datetime(end_date)
            if start_date is None or end_date is None:
                raise ValueError
        except ValueError:
            return Response({"error": "Invalid date format."}, status=status.HTTP_400_BAD_REQUEST)

        if start_date >= end_date:
            return Response({"error": "start_date must be before end_date."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            line = Line.objects.get(id=line_id)
        except Line.DoesNotExist:
            return Response({"error": "Line not found."}, status=status.HTTP_404_NOT_FOUND)

        # Calculate metrics
        production_logs = DaqLog.objects.filter(
            tag__machine__line_id=line_id,
            tag__name__icontains='Production',
            timestamp__range=(start_date, end_date)
        )
        
        downtime_logs = DaqLog.objects.filter(
            tag__machine__line_id=line_id,
            tag__name__icontains='Downtime',
            timestamp__range=(start_date, end_date)
        )

        quality_logs = DaqLog.objects.filter(
            tag__machine__line_id=line_id,
            tag__name__icontains='Quality',
            timestamp__range=(start_date, end_date)
        )

        total_time = (end_date - start_date).total_seconds() / 3600  # in hours
        
        production = production_logs.aggregate(total_production=Sum('value'))['total_production'] or 0
        downtime = downtime_logs.aggregate(total_downtime=Sum('value'))['total_downtime'] or 0
        
        production_rate = production / total_time if total_time > 0 else 0
        availability = (total_time - downtime) / total_time if total_time > 0 else 0
        
        # Efficiency calculation
        target_production = line.target_production * total_time
        efficiency = production / target_production if target_production > 0 else 0

        # Quality calculation
        good_products = quality_logs.filter(value__gte=0.95).aggregate(total=Sum('value'))['total'] or 0
        total_products = quality_logs.aggregate(total=Sum('value'))['total'] or 0
        quality = good_products / total_products if total_products > 0 else 0

        metrics = {
            "line_name": line.name,
            "production": production,
            "production_rate": production_rate,
            "efficiency": efficiency,
            "downtime": downtime,
            "availability": availability,
            "quality": quality
        }

        return Response(metrics, status=status.HTTP_200_OK)