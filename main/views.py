# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import ProductionLine, Tag, Log, Alert
from .serializers import ProductionLineSerializer, TagSerializer, LogSerializer, AlertSerializer
from django.utils.dateparse import parse_datetime
from django.db.models import Sum

class LogView(APIView):
    def get(self, request):
        line_id = request.query_params.get('LineId')
        tag_id = request.query_params.get('TagId')
        start_date = request.query_params.get('StartDate')
        end_date = request.query_params.get('EndDate')

        if not line_id or not tag_id or not start_date or not end_date:
            return Response(
                {"error": "LineId, TagId, StartDate, and EndDate are required."},
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

        queryset = Log.objects.filter(
            line_id=line_id,
            tag_id=tag_id,
            timestamp__range=(start_date, end_date)
        )

        serializer = LogSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

        production_lines = ProductionLine.objects.all()
        performance_data = []

        for line in production_lines:
            logs = Log.objects.filter(
                line=line,
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

class ProductionLineViewSet(viewsets.ModelViewSet):
    queryset = ProductionLine.objects.all()
    serializer_class = ProductionLineSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class LogViewSet(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
