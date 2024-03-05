from mainchat.models import Chating
from rest_framework import serializers

class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chating
        fields = ['id','room','content','username','timestamp']
        read_only_fields = ('id', 'timestamp')