from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import DO_NOTHING, PROTECT
from django.db.models.fields import CharField, IntegerField
from django.core.validators import MaxValueValidator, RegexValidator
from django.utils import tree

from . import validators

format_port = {
    "type2": "Type 2 ",
    "ccs": "CCS",
    "type1": "Type 1",
    "chademo": "CHAdeMO",
    "tesla_ccs": "CCS",
    "tesla_suc": "Tesla Supercharger"
}


 # Customer
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_expired_bills = models.BooleanField()

    def __str__(self):
        return f"Customer with ID:{self.id} and username {self.user.getusername()}"

 # Individual Bill 
class Bill(models.Model):
    customer = models.ForeignKey(User, related_name="bills", on_delete=models.CASCADE) # Many to One relationship with Customers
    date_created = models.DateTimeField(auto_now_add=True) # Updates automatically the time the object is saved
    total = models.FloatField()
    is_paid = models.BooleanField()

    def __str__(self):
        return f"Bill with ID:{self.id} belongs to {self.customer.get_username()}."

 # Monthly Bill expires every 1st of month
class MonthlyBill(models.Model):
    customer = models.ForeignKey(User, related_name="monthlybills", on_delete=models.CASCADE, null=True) # Many to One relationship with Customers
    monthly_total = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Monthly bill {self.start_date} to {self.end_date}."

 # Stored cards for customer
class Card(models.Model):
    customer = models.ForeignKey(User, related_name="cards", on_delete=models.CASCADE) # Many to One relationship with Customers
    card_no = models.IntegerField()

    def __str__(self):
        first_dig = self.card_no / 10000
        last_dig = self.card_no % 10000
        return f"{first_dig}********{last_dig}"

 # To represent class Car

 # Filled by reference 
class Ports(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"Port with ID: {self.id} and title {self.title}."

    @classmethod
    def create(cls, **kwargs):
        port = cls.objects.create(
            id=kwargs['ID'],
            title=kwargs['Title']
        )
        return port

# Filled by reference
class Brands(models.Model):
    id = models.CharField(max_length=100 ,primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Brand {self.name} has ID: {self.id}."

    @classmethod
    def create(cls, **kwargs):
        brand = cls.objects.create(
            id = kwargs['id'],
            name = kwargs['name']
        )
        return brand

# Filled by model 
class ACcharger(models.Model):
    usable_phases = models.IntegerField()
    ports = models.ManyToManyField(Ports) # Many to Many relationship to existing Ports
    max_power = models.FloatField()
    # Might want to insert power_per_charging_point afterwards

    def __str__(self):
        return f"AC charger with {self.usable_phases} phases, available ports: {self.ports} and {self.max_power} max power."

 # kwargs is data['data']['ac_charger']
    @classmethod
    def create(cls,**kwargs):
        charger = cls.objects.create(
            usable_phases = kwargs['usable_phases'],
            max_power = kwargs['max_power']
        )
        for i in kwargs['ports']:
            formatted_port = format_port[i]
            port = Ports.objects.filter(title__startswith=f"{formatted_port}")
            charger.ports.add(port)
        return charger

class chargingCurve(models.Model):
    percentage = models.FloatField(validators=[validators.validate_percentage])
    power = models.FloatField()

    def __str__(self):
        return f"Charging percentage {self.percentage} with power {self.power}."

class DCcharger(models.Model):
    ports = models.ManyToManyField(Ports) # Many to Many relationship to existing Ports
    max_power = models.FloatField()
    charging_curve = models.ManyToManyField(chargingCurve)

    def __str__(self):
        return f"DC charger with available ports: {self.ports}."

# kwargs is data['data']['dc_charger']
    @classmethod
    def create(cls,**kwargs):
        dcharger= cls.objects.create(
            max_power = kwargs['max_power']
        )
        for i in kwargs['ports']:
            formatted_port = format_port[i]
            port = Ports.objects.filter(title__startswith)=f"{formatted_port}"
            dcharger.ports.add(port)
        
        for i in kwargs['charging_curve']:
            curve = chargingCurve.objects.get_or_create(
                percentage=i['percentage'],
                power=i['power']
            )
            dcharger.charging_curve.add(curve)
        
        return dcharger

class Car(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    type = models.CharField(max_length=4)
    brand = models.OneToOneField(Brands, on_delete=PROTECT)
    model = models.CharField(max_length=100)
    release_year = models.IntegerField(validators=[validators.validate_year])
    usable_battery_size = models.FloatField(validators=[validators.validate_percentage])
    ac_charger = models.OneToOneField(ACcharger, on_delete=PROTECT)
    dc_charger = models.OneToOneField(DCcharger, on_delete=PROTECT)
    average_consumption = models.FloatField(validators=[validators.validate_percentage])
    customer = models.ForeignKey(User, related_name="cars", on_delete=models.CASCADE)

    def __str__(self):
        return f"Car with ID: {self.id},model {self.model} and type {self.type} belongs to {self.customer.get_username()}."

 # kwargs is data['data']
    @classmethod
    def create(cls,**kwargs):
        car = cls.objects.create(
            id = kwargs['id'],
            type = kwargs['type'],
            model = kwargs['model'],
            release_year = kwargs['release_year'],
            usable_battery_size = kwargs['usable_battery_size'],
            average_consumption = kwargs['energy_consumption']['average_consumption']
        )
        brand = Brands.objects.get(id=kwargs['brand_id'])
        car.brand.add(brand)
        ac_charger = ACcharger.create(**kwargs['ac_charger'])
        car.ac_charger.add(ac_charger)
        dc_charger = DCcharger.create(**kwargs['dc_charger'])
        car.dc_charger.add(dc_charger)
        
        return car

'''class Providers(models.Model):
    name = models.CharField(max_length=15)
<
    def __str__(self):
        return f"Provider is: {self.name}."'''
 
# To reprsent class Station
class Operator(models.Model):
    id = models.IntegerField(primary_key=True)
    website_url = models.URLField()
    contact_email = models.EmailField()
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"Operator {self.title}, website {self.website_url}, email {self.contact_email}."

# Filled by reference
class UsageType(models.Model):
    id = models.IntegerField(primary_key=True)
    Title = models.CharField(max_length=100)
    IsPayAtLocation = models.BooleanField(null=True)
    IsMembershipRequired = models.BooleanField(null=True)
    IsAccessKeyRequired = models.BooleanField(null=True)

    def __str__(self):
        return f"Is {self.Title}."

 # kwargs is data['Usage Types']
    @classmethod
    def create(cls,**kwargs):
        usagetype = cls.objects.create(
            id = kwargs['ID'],
            Title = kwargs['Title'],
            IsPayAtLocation = kwargs['IsPayAtLocation'],
            IsMembershipRequired = kwargs['IsMembershipRequired'],
            IsAccessKeyRequired = kwargs['IsAccessKeyRequired']
        )
        return usagetype
    
 # Filled by reference
class StatusType(models.Model):
    id = models.IntegerField(primary_key=True)
    Title = models.CharField(max_length=100)
    IsOperational = models.BooleanField(null=True)

    def __str__(self):
        return f"Is {self.Title}"

 # kwargs is data['StatusTypes']
    @classmethod
    def create(cls,**kwargs):
        status = cls.objects.create(
            id = kwargs['ID'],
            Title = kwargs['Title'],
            IsOperational = kwargs['IsOperational']
        )

 # Filled by station.create
class AddressInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    addressLine = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    stateOrProvince = models.CharField(max_length=100)
    postCode = models.IntegerField()
    countryId = models.IntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longtitude = models.DecimalField(max_digits=9, decimal_places=6)
    contact_telephone = models.CharField(max_length=13, null=True)
    access_comments = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return f"{self.addressLine}, {self.town}, {self.postCode}."

 # kwargs is data['AddressInfo']
    @classmethod
    def create(cls,**kwargs):
        address = cls.objects.create(
            id = kwargs['ID'],
            title = kwargs['Title'],
            addressLine = kwargs['AddressLine1'],
            town = kwargs['Town'],
            stateOrProvince = kwargs['StateOrProvince'],
            postCode = kwargs['Postcode'],
            countryID = kwargs['CountryID'],
            latitued = kwargs['Latitude'],
            longtitude = kwargs['Longtitude'],
            contact_telephone = kwargs['ContactTelephone1'],
            access_comments = kwargs['AccessComments']
        )
        return address

 # Filled by reference
class CurrentType(models.Model):
    id = models.IntegerField()
    title = models.CharField(max_length=50)

    def __str__(self):
        return f"Current type of {self.title}."

 # kwargs is data['CurrentTypes']
    @classmethod
    def create(cls,**kwargs):
        currType = cls.objects.create(
            id = kwargs['ID'],
            title = kwargs['Title']
        )
        return currType

 # Filled by stations.create
class Connections(models.Model):
    id = models.IntegerField(primary_key=True)
    ports = models.ManyToManyField(Ports, related_name="exist_at")
    current_type = models.ManyToManyField(CurrentType, related_name="exists_at", null=True)
    voltage = models.IntegerField(null=True)
    powerKW = models.FloatField()
    quantity = models.IntegerField()
    status_type = models.ForeignKey(StatusType) #One status type to many connections

    def __str__(self):
        return f"{self.quantity} connections."
     

class Station(models.Model):
    id = models.IntegerField(primary_key=True)
    operators = models.ManyToManyField(Operator, related_name="operates")
    connections = models.OneToOneField(Connections)
    usageType = models.ForeignKey(UsageType)
    statusType = models.ForeignKey(StatusType)
    addressInfo = models.OneToOneField(AddressInfo,related_name="belongs_to",on_delete=models.CASCADE)
    photo = models.URLField(null=True)
    #userComments in UserComments table, accessed by station.UserComments
    generalComments = models.CharField(max_length=1000, null=True) 
    
    def __str__(self):
        return f"Station with ports {self.ports} ports at {self.addressInfo}."

# kwargs is data
    @classmethod
    def create(cls,**kwargs):
        station = cls.objects.create(
            id = kwargs['ID'],
            photo = kwargs['MediaItems']['ItemURL'], #Might have multiple media items MUST BUG FIX
            generalComments = kwargs['GeneralComments'])

        opInfo = kwargs['OperatorInfo']
        operator = Operator.objects.get_or_create(
            id = opInfo['ID'],
            website_url = opInfo['WebsiteURL'],
            contact_email = opInfo['ContactEmail'],
            title = opInfo['Title']
        )
        station.operators.add(operator)
        
        connectionsInfo = kwargs['Connections']
        for i in connectionsInfo:
            connection = Connections.objects.get_or_create(
                id = i['ID'],
                voltage = i['Voltage'],
                powerKW = i['PowerKW'],
                quantity = i['Quantity']
            )
            port = Ports.objects.get(id)

        
        return station

    @property
    def rating(self):
        count=0
        rating=0
        allComms = UserComments.objects.select_related('rating').filter(station__id=self.id)
        
        for i in allComms:
            rating += i.rating
            count += 1
        
        return rating/count
            

class CheckinStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)

class UserComments(models.Model):
    station = models.ForeignKey(Station, related_name="UserComments")
    username = models.CharField(max_length=100)
    comment = models.CharField(max_length=1000)
    rating = models.IntegerField()
    customer = models.ForeignKey(User, related_name="myComments",on_delete=models.CASCADE, null=True)
    checkinStatus = models.ManyToManyField(CheckinStatus)

class Session(models.Model):
    customer = models.ForeignKey(User, related_name="sessions", on_delete=models.CASCADE)
    #provider = models.CharField(max_length=1, choices=PROVIDERS)
    duration = models.TimeField()
    total_kwh = models.FloatField()
    cost = models.FloatField()

    def __str__(self):
        return f"Charged with {self.provider.get_provider_display} for {self.duration}, transfered totally {self.total_kwh} KWh for {self.cost} euros."
        