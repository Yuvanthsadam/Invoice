from rest_framework import serializers
from billing.models import *
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=68, min_length=4, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')


class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Admin
        fields = '__all__'
        extra_kwargs = {
            "profile_image": {
                "required": False,
            }
        }
        # fields = ('user','id', 'first_name', 'last_name','phone_number','gender','email','password')

class Sub_Title_Two_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Sub_Title_Two
        fields = ['sub_title_one','sub_title_two','id','quantity','price', 'description']

class Sub_Title_One_Serializer(serializers.ModelSerializer):
    sub_title_two = Sub_Title_Two_Serializer(read_only=True, many=True)
    
    class Meta:
        model = Sub_Title_One
        fields = ['main','id','sub_title_one','quantity','price', 'description','sub_title_two']

class MainSerializer(serializers.ModelSerializer):
    sub_title_one = Sub_Title_One_Serializer(read_only=True, many=True)
    class Meta:
        model = Main
        fields = ['admin_id','id', 'main_title', 'description','sub_title_one']


class AdminRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    email = serializers.EmailField(max_length=75, allow_blank=False)
    password = serializers.CharField(
        max_length=75, allow_blank=False, trim_whitespace=True)

    class Meta:
        model = Admin
        fields = '__all__'
    
    # validating Email
    def validate_email(self, email):
        user = User.objects.filter(email=(email)).exists()

        if user:
            raise serializers.ValidationError("Email Already registered")
        return email

    # validating password
    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError("password too Short!!")
        return password
    
    def create(self, validated_data, *args, **kwargs):
        user = User.objects.create_user(email = validated_data.pop('email'),password= validated_data.pop('password'))
        user.is_admin = True
        user.save()
        admin = Admin.objects.create(user=user, **validated_data)
        return admin
    
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect Credentials Passed.')
    

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
class ProductSerializer(serializers.ModelSerializer):
    main = MainSerializer(read_only=True, many=True)
    
    class Meta:
        model = Product
        fields = '__all__' 

class DraftedSerializer(serializers.ModelSerializer):
    main = MainSerializer(read_only=True, many=True)
    
    class Meta:
        model = Drafted
        fields = ['id', 'drafted_product', 'main']
        
class PendingSerializer(serializers.ModelSerializer):
    main = MainSerializer(read_only=True, many=True)
    
    class Meta:
        model = Pending
        fields = '__all__' 
        

class CompletedSerializer(serializers.ModelSerializer):
    main = MainSerializer(read_only=True, many=True)
    
    class Meta:
        model = Completed
        fields = '__all__' 
        
class StoringPDFSerializer(serializers.ModelSerializer):    
    class Meta:
        model = StoringPDF
        fields = ('id','storing_pdf')
        # fields = '__all__'