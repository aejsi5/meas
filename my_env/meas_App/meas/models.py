from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Currency(models.Model):
    Currency_id = models.AutoField('ID', primary_key= True)
    Currency_name = models.CharField('Währungsname', max_length=30)
    Currency_symbol = models.CharField('Währungssymbol', max_length=30)

    def __str__(self):
        return str(self.Currency_name)
    
    class Meta:
        app_label ="meas"
        ordering = ['Currency_id']

class Mandant(models.Model):
    Mandant_id = models.AutoField('ID', primary_key= True)
    Mandant_accn= models.CharField('Kundennummer', max_length=10)
    Mandant_name = models.CharField('Bezeichnung', max_length=200)
    Mandant_street = models.CharField('Straße', max_length=200, null=True, blank=True)
    Mandant_zip = models.CharField('PLZ', max_length=10, null=True, blank=True)
    Mandant_city = models.CharField('Ort', max_length=200, null=True, blank=True)
    Mandant_iban = models.CharField('IBAN', max_length=200, null=True, blank=True)
    Mandant_bic = models.CharField('BIC', max_length=200, null=True, blank=True)
    Mandant_ustid = models.CharField('UstID', max_length=200, null=True, blank=True)
    Currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null = True)
    Mandant_vf = models.DateTimeField('Gültig von', default=now)
    Mandant_vu = models.DateTimeField('Gültig bis', null=True, blank=True)
    Mandant_ia = models.DateTimeField('Hinzugefügt am', auto_now=True)
    Mandant_deleted = models.BooleanField('Gelöscht', default=False)
    
    def __str__(self):
        return str(self.Mandant_id)
    
    class Meta:
        app_label ="meas"
        ordering = ['Mandant_ia']

class Meas_User(AbstractUser):
    Mandant = models.ForeignKey(Mandant, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return self.username

class Employee(models.Model):
    Employees_id = models.AutoField('ID', primary_key=True)
    Mandant = models.ForeignKey(Mandant, on_delete=models.CASCADE)
    Employees_acn = models.CharField('Mitarbeiternummer', max_length=10)
    Employees_first = models.CharField('Vorname', max_length=200)
    Employees_last = models.CharField('Nachname', max_length=200)
    Employees_birthday = models.DateField('Geburtstag', null=True, blank=True)
    Employees_phone = models.CharField('Telefon', max_length=20, null=True, blank=True)
    Employees_mail = models.EmailField('E-Mail', null=True, blank=True)
    Employees_vf = models.DateTimeField('Gültig von', default=now)
    Employees_vu = models.DateTimeField('Gültig bis', null=True, blank=True)
    Employees_ia = models.DateTimeField('Hinzugefügt am', auto_now=True)
    Employees_deleted = models.BooleanField('Gelöscht', default=False)
    
    def __str__(self):
        return self.Employees_last

    class Meta:
        app_label ="meas"
        ordering = ['Employees_last']

class Customer(models.Model):
    Customer_id= models.AutoField('ID', primary_key=True)
    Mandant = models.ForeignKey(Mandant, on_delete=models.CASCADE)
    Customer_acn = models.CharField('Kundennummer', max_length=10)
    Customer_company = models.CharField('Firma', max_length=200, null=True, blank=True)
    Customer_first = models.CharField('Vorname', max_length=200, null=True, blank=True)
    Customer_last = models.CharField('Nachname', max_length=200, null=True, blank=True)
    Customer_street = models.CharField('Straße', max_length=200, null=True, blank=True)
    Customer_zip = models.CharField('PLZ', max_length=5, null=True, blank=True)
    Customer_city = models.CharField('Stadt', max_length=200, null=True, blank=True)
    Customer_phone = models.CharField('Telefon', max_length=20, null=True, blank=True)
    Customer_mail = models.EmailField('E-Mail', null=True, blank=True)
    Customer_ustid = models.CharField('UstID', max_length=50, null= True, blank = True)
    Customer_ia = models.DateTimeField('Hinzugefügt am', default=now)
    Customer_deleted = models.BooleanField('Gelöscht', default=False)

    def __str__(self):
        return self.Customer_acn
    
    class Meta:
        app_label = "meas"

class Customer_Project(models.Model):
    CP_id = models.AutoField('ID', primary_key=True)
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    CP_number = models.CharField('Bauvorhaben', max_length=10)
    CP_address = models.CharField('Adresse', max_length=200)
    CP_address_add = models.CharField('Adresszusatz', max_length=200, blank=True, null=True)
    CP_zip = models.CharField('PLZ', max_length=5)
    CP_city = models.CharField('Stadt', max_length=200)
    CP_contact = models.CharField('Ansprechpartner', max_length=200, blank=True, null=True)
    CP_contact_phone = models.CharField('Ansprechpartner Telefon', max_length=200, blank=True, null=True)
    CP_contact_mail = models.EmailField('Ansprechpartner E-Mail', blank=True, null=True)

    def __str__(self):
        return self.CP_number

    class Meta:
        app_label = "meas"

class Unit(models.Model):
    Unit_id = models.AutoField('ID', primary_key=True)
    Unit_symbol = models.CharField('Einheitssymbol', max_length=5, null=False, blank=False)
    Unit_name = models.CharField('Einheitsname', max_length=50, null=False, blank=False)
    Unit_desc = models.CharField('Einheitsbeschreibung', max_length=200, null=True, blank=True)

    def __str__(self):
        return self.Unit_name
    
    class Meta:
        app_label ="meas"

class Product(models.Model):
    Product_id = models.AutoField('ID', primary_key=True)
    Mandant = models.ForeignKey(Mandant, on_delete=models.CASCADE)
    Product_number = models.CharField('Artikelnummer', max_length=200, null=False, blank=False)
    Product_name = models.CharField('Artikelbezeichnung', max_length=200, null=True, blank=True)
    Product_desc = models.CharField('Beschreibung', max_length=254, null=True, blank=True)
    Product_supplier = models.CharField('Lieferant', max_length=200, null=True, blank=True)
    Product_supplier_code = models.CharField('Lieferantennummer', max_length=200, null=True, blank=True)
    Product_unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    Product_pppu_net = models.DecimalField('Einkaufspreis pro Einheit (netto)',max_digits=6, decimal_places=2)
    Product_sppu_net = models.DecimalField('Verkaufspreis pro Einheit (netto)',max_digits=6, decimal_places=2)
    Product_vf = models.DateTimeField('Gültig von', default=now)
    Product_vu = models.DateTimeField('Gültig bis', null=True, blank=True)
    Product_ia = models.DateTimeField('Hinzugefügt am', auto_now=True)
    Product_deleted = models.BooleanField('Gelöscht', default=False)

    def __str__(self):
        return self.Product_name
    
    class Meta:
        app_label ="meas"

class Service(models.Model):
    Service_id = models.AutoField('ID', primary_key=True)
    Mandant = models.ForeignKey(Mandant, on_delete=models.CASCADE)
    Service_number = models.CharField('Arbeitspositions-Nummer', max_length=200, null=False, blank=False)
    Service_name = models.CharField('Arbeitspositionsbezeichnung', max_length=200, null=False, blank=False)
    Service_duration = models.DecimalField('Zeiteinheiten',max_length=6, decimal_places=2)
    Service_vf = models.DateTimeField('Gültig von', default=now)
    Service_vu = models.DateTimeField('Gültig bis', null=True, blank=True)
    Service_ia = models.DateTimeField('Hinzugefügt am', auto_now=True)
    Service_deleted = models.BooleanField('Gelöscht', default=False)

    def __str__(self):
        return self.Service_name
    
    class Meta:
        app_label ="meas"
    
class Order(models.Model):
    Order_id = models.AutoField('ID', primary_key=True)
    Mandant = models.ForeignKey(Mandant, on_delete=models.CASCADE)
    Employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    CP = models.ForeignKey(Customer_Project, on_delete=models.CASCADE)
    Order_number = models.CharField('Auftragsnummer', max_length=200)
    Order_creation_date = models.DateTimeField('Anlagedatum', auto_now_add=True)
    Order_input_channel = models.CharField(max_length=200, null=True, blank=True)
    Order_desc = models.CharField(max_length=254, null = True, blank = True)
    Order_date_sch = models.DateField('Auftragsdatum geplant', null = True, blank = True)
    Order_time_sch = models.TimeField('Auftragsuhrzeit geplant', null=True, blank=True)
    Order_date_act = models.DateField('Auftragsdatum  tatsächlich', null = True, blank = True)
    Order_time_act = models.TimeField('Auftragsuhrzeit tatsächlich', null=True, blank=True)
    Order_provision_date = models.DateField('Bereitstellungsdatum', null=True, blank=True)
    Order_provision_time = models.TimeField('Bereitstellungsuhrzeit', null=True, blank=True)
    Order_accepted = models.BooleanField('Angenommen', default=False)

    def __str__(self):
        return self.Order_number
    
    class Meta:
        app_label ="meas"

def signature_directory_path(instance,filename):
        return 'aufmass_unterschrift_{0}/{1}'.format(instance.Measurement_number,filename)

class Measurement(models.Model):
    Measurement_id = models.AutoField('ID', primary_key=True)
    Order = models.ForeignKey(Order, on_delete=models.CASCADE)
    #Product = models.ManyToManyField(Product, through="Measurement_Product", symmetrical=False)
    Measurement_number =  models.CharField('Aufmaßnummer', max_length=200)
    Measurement_creation_date = models.DateTimeField('Anlagedatum', auto_now_add=True)
    Measurement_desc = models.CharField('Aufmaßnotiz', max_length=254, blank=True, null=True)
    Measurement_signed_by = models.CharField('Unterschrieben von', max_length=200, blank=True, null=True)
    Measurement_signature = models.FileField('Unterschrift', upload_to=signature_directory_path, blank=True, null=True)
    Measurement_editable = models.BooleanField('Abgeschlossen', default=False)

    def __str__(self):
        return self.Measurement_number

    class Meta:
        app_label="meas"

class Measurement_Product(models.Model):
    MP_id = models.AutoField('ID', primary_key=True)
    Measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    MP_quantity = models.FloatField('Menge', blank=True, null=True)
    MP_ia = models.DateTimeField('Hinzugefügt am', auto_now=True)
    MP_deleted = models.BooleanField('Gelöscht', default=False)

    class Meta:
        app_label="meas"

class Timesheet_Type(models.Model):
    Timesheet_Type_id = models.AutoField('ID', primary_key=True)
    Mandant = models.ForeignKey(Mandant, on_delete=models.CASCADE)
    Timesheet_Type_name = models.CharField('Art', max_length=200, null=True, blank=True)
    Timesheet_Type_desc = models.CharField('Art Beschreibung', max_length=200, null=True, blank=True)
    Timesheet_Type_ia = models.DateTimeField('Hinzugefügt am', auto_now=True)
    Timesheet_Type_deleted = models.BooleanField('Gelöscht', default=False)

    def __str__(self):
        return self.Timesheet_Type_name
    
    class Meta:
        app_label ="meas"

class Timesheet(models.Model):
    Timesheet_id = models.AutoField('ID', primary_key=True)
    Employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    Timesheet_number = models.CharField('Stundenzettelnummer', max_length=10)
    Timesheet_creation_date = models.DateTimeField('Hinzugefügt am', auto_now=True)
    Timesheet_type = models.ForeignKey(Timesheet_Type, on_delete=models.CASCADE)
    Timesheet_date_start = models.DateField('Start Datum', default=now, null=True, blank=True)
    Timesheet_time_start = models.TimeField('Start Uhrzeit', default=now, null=True, blank=True)
    Timesheet_date_end = models.DateField('Ende Datum', null=True, blank=True)
    Timesheet_time_end = models.TimeField('Ende Uhrzeit', null=True, blank=True)
    Timesheet_deleted = models.BooleanField('Gelöscht', default=False)

    def __str__(self):
        return self.Timesheet_number
    
    class Meta:
        app_label ="meas"

    



