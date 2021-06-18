from payesh.dynamic import api_error_creator
from payesh.dynamic_api import DynamicSerializer
from ticket.models import Ticket, Message


class TicketCreateSerializer(DynamicSerializer):
    remove_field_view = {
    }

    class Meta:
        model = Ticket
        extra_kwargs = api_error_creator(Ticket,
                                         ['user', 'title', 'created_at', 'is_closed', ],
                                         blank_fields=['user'],
                                         required_fields=[])
        depth = 5
        fields = ['id', 'user', 'title', 'created_at', 'is_closed', ]

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class MessageCreateSerializer(DynamicSerializer):
    remove_field_view = {
    }

    class Meta:
        model = Message
        extra_kwargs = api_error_creator(Message,
                                         ['ticket', 'text', 'user', 'file', 'is_seen', 'is_seen_by_admin',
                                          'created_at', ],
                                         blank_fields=['ticket', 'user'],
                                         required_fields=[])
        depth = 5
        fields = ['id', 'ticket', 'text', 'user', 'file', 'is_seen', 'is_seen_by_admin', 'created_at', ]

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        if user.is_student():
            validated_data['is_seen'] = True
        else:
            validated_data['is_seen_by_admin'] = True
        return super().create(validated_data)
