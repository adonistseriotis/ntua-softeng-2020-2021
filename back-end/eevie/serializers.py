from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
from eevie.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        Customer.objects.create(user=instance,has_expired_bills=False)
        return instance

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token['username'] = user.username
        return token

'''class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('token', 'username', 'password')

    def get_token(self,obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance'''
    
class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Customer
        fields = '__all__'

    def get_user(self, obj):
       data =  UserSerializer(obj.user).data
       return data

    def create(self, validated_data):
        print("OMG")
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user = User(**user_data)

        if password is not None:
            user.set_password(password)
        user.save()
        customer = Customer.objects.create(user=user,**validated_data)
        customer.save()
        return customer

    def update(self, instance, validated_data):
        print("LOCO")
        user_data = validated_data.pop('user')
        user = UserSerializer()
        super(CustomerSerializer,self).update(instance,validated_data)
        super(UserSerializer,user).update(instance.user,user_data)
        return instance

    
class BillSerializer(serializers.ModelSerializer):
    customer = ReadOnlyField(source='customer.id')

    class Meta:
        model=Bill
        fields='__all__'
