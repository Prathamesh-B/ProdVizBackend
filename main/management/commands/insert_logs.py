import pandas as pd
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from main.models import ProductionLine, Tag, Log

class Command(BaseCommand):
    help = 'Imports data from an Excel file into the database'

    def handle(self, *args, **kwargs):
        file_path = 'main/management/commands/log_data_15min_interval_new_v5.xlsx'
        log_data = pd.read_excel(file_path, sheet_name='Log')
        
        now = timezone.now()
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        current_timestamp = start_date

        timestamps = []

        for day in range(7):
            for record_set in range(96):
                timestamps.extend([current_timestamp] * 96)
                current_timestamp += timedelta(minutes=15)

        if len(timestamps) != len(log_data):
            self.stdout.write(self.style.ERROR("The number of generated timestamps does not match the number of records in the Excel sheet."))
            return
        
        for i, (_, row) in enumerate(log_data.iterrows()):
            line = ProductionLine.objects.get(id=row['line_id'])
            tag = Tag.objects.get(id=row['tag_id'])
            
            Log.objects.create(
                timestamp=timestamps[i],
                line=line,
                tag=tag,
                value=row['value'],
                inactive=row['inactive'],
                modified=row['modified']
            )

        self.stdout.write(self.style.SUCCESS('Data import completed successfully.'))
