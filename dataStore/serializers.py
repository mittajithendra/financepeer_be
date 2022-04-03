from rest_framework import serializers
from .models import Blog,User

class BlogItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ('__all__')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','username','password']
        extra_kwargs = {
            'password': {'write_only':True}
        }
    
        def create(self,validated_data):
            password = validated_data.pop('password',None)
            instance = self.Meta.model(**validated_data)
            if(password is not None):
                instance.set_password(password)
            instance.save()
            return instance