from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from abresani.dynamic import api_error_creator
from abresani.dynamic_api import DynamicSerializer
from user.models import User


class UserCreateSerializer(DynamicSerializer):
    """
    برای ایجاد کاربر جدید در سامانه
    """
    remove_field_view = {
        'retrieve': ['password'],
        'self': ['password', 'is_confirmed', 'groups']
    }

    class Meta:
        model = User
        extra_kwargs = api_error_creator(User,
                                         ['username', 'password', 'first_name', 'last_name', 'mobile_number', 'groups'],
                                         blank_fields=['username', 'password'],
                                         required_fields=['first_name', 'last_name', 'mobile_number'])
        depth = 5
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'mobile_number', 'is_confirmed', 'groups']

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def validate_password(self, value):
        return make_password(value)

    def validate_username(self, value):
        if self.context['view'].action == 'create':
            if value is None or value == '':
                raise serializers.ValidationError('نام کاربری باید وارد شود')
        return value


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    این کلاس برای ثبت نام کاربر استفاده می شود .
    فیلد هایی که برای ثبت کاربر مورد استفاده قرار می گیرد عبارتند از :

    #.
        نام کاربری
    #.
     ایمیل
    #.
      پسورد
    """
    repeat_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        extra_kwargs = api_error_creator(User, ['username', 'password', 'first_name', 'last_name'],
                                         required_fields=['username', 'password', 'first_name', 'last_name'])
        fields = ['username', 'first_name', 'last_name', 'repeat_password', 'password']

    def create(self, validated_data):
        """
        برای ایجاد ساخت کاربر جدید در سامانه و  مورد استفاده قرار می گیرد .

        Arguments:
         validated_data:
             چک کردن صحت داده ها
        :return:
          کاربر ثبت نام شده بر گردانده می شود .
        """

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],

        )
        return validated_data

    def validate_password(self, value):
        data = self.get_initial()
        repeat_password = data.get('repeat_password')
        password = value
        password = data.get('password')

        if password != repeat_password:
            raise serializers.ValidationError('رمز عبور با تکرار رمز عبور یکسان نیست')
        if password is None or password == '':
            raise serializers.ValidationError('رمز عبور باید وارد شود')

        if password != repeat_password:
            raise serializers.ValidationError('رمز عبور با تکرار رمز عبور یکسان نیست')
        return value
