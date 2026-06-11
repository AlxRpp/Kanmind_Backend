from rest_framework import serializers
from ..models import Boards
from django.contrib.auth.models import User


class BoardSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True,
        required=False
    )

    def get_member_count(self, obj):
        return obj.members.count()

    def get_ticket_count(self, obj):
        return 0

    def get_tasks_to_do_count(self, obj):
        return 0

    def get_tasks_high_prio_count(self, obj):
        return 0

    class Meta:
        model = Boards
        fields = ['id', 'title', 'members', 'member_count',
                  'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id']


class GetSingleBoardSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()

    def get_members(self, obj):
        return [
            {'id': u.id, 'email': u.email, 'fullname': u.username}
            for u in obj.members.all()
        ]

    def get_tasks(self, obj):
        return [{'title': 'CommingSoon'}]

    class Meta:
        model = Boards
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']


class WriteAndDeleteSingleBoardSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        write_only=True,
        many=True,
        required=False,
        queryset=User.objects.all()
    )
    owner_data = serializers.SerializerMethodField()
    members_data = serializers.SerializerMethodField()

    def get_owner_data(self, obj):
        return {'id': obj.owner.id, 'email': obj.owner.email, 'fullname': obj.owner.username}

    def get_members_data(self, obj):
        return [{'id': u.id, 'email': u.email, 'fullname': u.username}
                for u in obj.members.all()]

    class Meta:
        model = Boards
        fields = ['id', 'title', 'owner_data', 'members', 'members_data']


class EmailCheckSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source='username')

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']
