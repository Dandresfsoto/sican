from rest_framework import serializers
from usuarios.models import User
from inbox.models import Mensaje

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','fullname','email','get_photo')

class MensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','user','created','leido','de','para','texto','adjuntos')