import pandas as pd
from django.core.management.base import BaseCommand
from main.models import ProductionLine, Tag, Log, Alert

class Command(BaseCommand):
    help = 'Imports data from an Excel file into the database'

    def handle(self, *args, **kwargs):
        # Load the Excel file
        file_path = 'main\management\commands\log_data_15min_interval_new_v5.xlsx'
        excel_data = pd.ExcelFile(file_path)

        # Import data from the 'ProductionLine' sheet
        if 'ProductionLine' in excel_data.sheet_names:
            pl_data = pd.read_excel(file_path, sheet_name='ProductionLine')
            for _, row in pl_data.iterrows():
                ProductionLine.objects.update_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'status': row['status'],
                        'inactive': row['inactive'],
                        'modified': row['modified']
                    }
                )

        # Import data from the 'Tag' sheet
        if 'Tag' in excel_data.sheet_names:
            tag_data = pd.read_excel(file_path, sheet_name='Tag')
            for _, row in tag_data.iterrows():
                Tag.objects.update_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'units': row['units'],
                        'min_val': row['min_val'],
                        'max_val': row['max_val'],
                        'inactive': row['inactive'],
                        'modified': row['modified']
                    }
                )

        # Import data from the 'Log' sheet
        if 'Log' in excel_data.sheet_names:
            log_data = pd.read_excel(file_path, sheet_name='Log')
            for _, row in log_data.iterrows():
                line = ProductionLine.objects.get(id=row['line_id'])
                tag = Tag.objects.get(id=row['tag_id'])
                Log.objects.update_or_create(
                    id=row['id'],
                    defaults={
                        'timestamp': row['timestamp'],
                        'line': line,
                        'tag': tag,
                        'value': row['value'],
                        'inactive': row['inactive'],
                        'modified': row['modified']
                    }
                )

        # Import data from the 'Alert' sheet
        if 'Alert' in excel_data.sheet_names:
            alert_data = pd.read_excel(file_path, sheet_name='Alert')
            for _, row in alert_data.iterrows():
                line = ProductionLine.objects.get(id=row['line_id'])
                tag = Tag.objects.get(id=row['tag_id'])
                Alert.objects.update_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'type': row['type'],
                        'timestamp': row['timestamp'],
                        'line': line,
                        'tag': tag,
                        'report_title': row['report_title'],
                        'report_type': row['report_type'],
                        'report_category': row['report_category'],
                        'report_sub_cat': row['report_sub_cat'],
                        'location': row['location'],
                        'incident_dtls': row['incident_dtls'],
                        'issued': row['issued'],
                        'role': row['role'],
                        'inactive': row['inactive'],
                        'modified': row['modified']
                    }
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported data from Excel file'))
