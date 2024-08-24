from django.db import models

class AuthRole(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    inactive = models.BooleanField(default=False)

    class Meta:
        db_table = 'ap_AuthRole'
        verbose_name = "ap_AuthRole"
        verbose_name_plural = "ap_AuthRoles"

    def __str__(self):
        return self.name


class AuthUser(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.ForeignKey(AuthRole, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    inactive = models.BooleanField(default=False)

    class Meta:
        db_table = 'ap_AuthUser'
        verbose_name = "ap_AuthUser"
        verbose_name_plural = "ap_AuthUsers"

    def __str__(self):
        return self.name


class Plant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    inactive = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ap_Plant'
        verbose_name = "ap_Plant"
        verbose_name_plural = "ap_Plants"

    def __str__(self):
        return self.name


class Block(models.Model):
    id = models.AutoField(primary_key=True)
    plant = models.ForeignKey(Plant, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    inactive = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ap_Block'
        verbose_name = "ap_Block"
        verbose_name_plural = "ap_Blocks"

    def __str__(self):
        return f"{self.plant.name} - {self.name}"


class Line(models.Model):
    id = models.AutoField(primary_key=True)
    block = models.ForeignKey(Block, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    target_production = models.IntegerField(default=0)
    status = models.CharField(max_length=50)
    inactive = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ap_Line'
        verbose_name = "ap_Line"
        verbose_name_plural = "ap_Lines"

    def __str__(self):
        return f"{self.block.plant.name} - {self.block.name} - {self.name} - {self.status}"


class Machine(models.Model):
    id = models.AutoField(primary_key=True)
    line = models.ForeignKey(Line, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    height_px = models.IntegerField()
    width_px = models.IntegerField()
    x_coordinate = models.IntegerField()
    y_coordinate = models.IntegerField()
    inactive = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ap_Machine'
        verbose_name = "ap_Machine"
        verbose_name_plural = "ap_Machines"

    def __str__(self):
        return f"{self.line.block.plant.name} - {self.line.block.name} - {self.line.name} - {self.name} - {self.status}"


class SensorTagType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    units = models.CharField(max_length=10)
    inactive = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ap_SensorTagType'
        verbose_name = "ap_SensorTagType"
        verbose_name_plural = "ap_SensorTagTypes"

    def __str__(self):
        return self.name


class SensorTag(models.Model):
    id = models.AutoField(primary_key=True)
    machine = models.ForeignKey(Machine, on_delete=models.DO_NOTHING)
    tag_type = models.ForeignKey(SensorTagType, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    min_val = models.FloatField()
    max_val = models.FloatField()
    nominal_val = models.FloatField(null=True, blank=True)
    threshold_alert = models.CharField(max_length=100)
    continuous_record = models.BooleanField(default=False)
    frequency = models.CharField(max_length=100, null=True, blank=True)
    inactive = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ap_SensorTag'
        verbose_name = "ap_SensorTag"
        verbose_name_plural = "ap_SensorTags"

    def __str__(self):
        return f"{self.machine.line.block.plant.name} - {self.machine.line.block.name} - {self.machine.line.name} - {self.machine.name} - {self.name}"


class DaqLog(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField()
    tag = models.ForeignKey(SensorTag, on_delete=models.DO_NOTHING)
    value = models.FloatField()
    inactive = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ap_DaqLog'
        verbose_name = "ap_DaqLog"
        verbose_name_plural = "ap_DaqLogs"

    def __str__(self):
        return f"{self.timestamp} - {self.tag.machine.line.block.plant.name} - {self.tag.machine.line.name} - {self.tag.machine.name} - {self.tag.name} - {self.value}"


class Alert(models.Model):
    id = models.AutoField(primary_key=True)
    line = models.ForeignKey(Line, on_delete=models.DO_NOTHING)
    tag = models.ForeignKey(SensorTag, on_delete=models.DO_NOTHING)
    timestamp = models.TimeField()
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, default='info')
    inactive = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ap_Alert'
        verbose_name = "ap_Alert"
        verbose_name_plural = "ap_Alerts"

    def __str__(self):
        return f"{self.line.block.plant.name} - {self.line.block.name} - {self.line.name} - {self.tag.name} - {self.timestamp} - {self.name}"


class Incident(models.Model):
    id = models.AutoField(primary_key=True)
    alert = models.ForeignKey(Alert, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    location = models.ForeignKey(Block, on_delete=models.DO_NOTHING)
    line = models.ForeignKey(Line, on_delete=models.DO_NOTHING)
    tag = models.ForeignKey(SensorTag, on_delete=models.DO_NOTHING)
    date = models.DateField()
    open = models.BooleanField(default=True)
    inactive = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ap_Incident'
        verbose_name = "ap_Incident"
        verbose_name_plural = "ap_Incidents"

    def __str__(self):
        return f"{self.date} - {self.title}"


class IncidentTransaction(models.Model):
    id = models.AutoField(primary_key=True)
    incident = models.ForeignKey(Incident, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField()
    issued_by = models.ForeignKey(AuthUser, on_delete=models.DO_NOTHING)
    msg = models.TextField(null=True, blank=True)
    inactive = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ap_IncidentTransaction'
        verbose_name = "ap_IncidentTransaction"
        verbose_name_plural = "ap_IncidentTransactions"

    def __str__(self):
        return f"{self.timestamp} - {self.issued_by.name} - {self.msg}"