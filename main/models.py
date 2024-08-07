from django.db import models
from django.utils import timezone

class ProductionLine(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    inactive = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ap_ProductionLine'
        verbose_name = "ap_ProductionLine"
        verbose_name_plural = "ap_ProductionLines"

    def __str__(self):
        return self.name

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    units = models.CharField(max_length=50)
    min_val = models.IntegerField()
    max_val = models.IntegerField()
    inactive = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ap_Tag'
        verbose_name = "ap_Tag"
        verbose_name_plural = "ap_Tags"

    def __str__(self):
        return self.name

class Log(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(default=timezone.now)
    line = models.ForeignKey(ProductionLine, on_delete=models.DO_NOTHING, null=True)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING, null=True)
    value = models.IntegerField()
    inactive = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ap_Log'
        verbose_name = "ap_Log"
        verbose_name_plural = "ap_Logs"

    def __str__(self):
        return f"{self.timestamp} - {self.line.name} - {self.tag.name}"

class Alert(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    line = models.ForeignKey(ProductionLine, on_delete=models.DO_NOTHING, null=True)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING, null=True)
    report_title = models.CharField(max_length=255, null=True)
    severity = models.CharField(max_length=255, null=True)
    report_type = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    report_category = models.CharField(max_length=255, null=True)
    report_sub_cat = models.CharField(max_length=255, null=True)
    incident_dtls = models.CharField(max_length=1000, null=True)
    resolve_date = models.DateField(null=True)
    issued = models.CharField(max_length=255, null=True)
    role = models.CharField(max_length=255, null=True)
    inactive = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ap_Alert'
        verbose_name = "ap_Alert"
        verbose_name_plural = "ap_Alerts"

    def __str__(self):
        return f"{self.name} - {self.type} - {self.timestamp}"
