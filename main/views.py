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
