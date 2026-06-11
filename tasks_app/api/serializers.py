from rest_framework import serializers
from boards_app.models import Boards
from django.contrib.auth.models import User
from ..models import Tasks


class PostTaskSerializer(serializers.ModelSerializer):
    board = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Boards.objects.all(),
        required=True
    )

    assignee_id = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=User.objects.all(),
        required=True,
        write_only=True,
        source='assignee'
    )
    assignee = serializers.SerializerMethodField()

    reviewer_id = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=User.objects.all(),
        required=True,
        write_only=True,
        source='reviewer'
    )

    reviewer = serializers.SerializerMethodField()

    comments_count = serializers.SerializerMethodField()

    def get_assignee(self, obj):
        return {'id': obj.assignee.id, 'email': obj.assignee.email,
                'fullname': obj.assignee.username}

    def get_reviewer(self, obj):
        return {'id': obj.reviewer.id, 'email': obj.reviewer.email,
                'fullname': obj.reviewer.username}

    def get_comments_count(self, obj):
        return 0

    class Meta:
        model = Tasks
        fields = ['id', 'board', 'title', 'description', 'status',
                  'priority', 'assignee', 'reviewer', 'comments_count', 'assignee_id', 'reviewer_id', 'due_date']


class UpdateAndDeleteTaskSerializer(serializers.ModelSerializer):
    board = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True
    )

    assignee_id = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=User.objects.all(),
        required=True,
        write_only=True,
        source='assignee'
    )
    assignee = serializers.SerializerMethodField()

    reviewer_id = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=User.objects.all(),
        required=True,
        write_only=True,
        source='reviewer'
    )

    reviewer = serializers.SerializerMethodField()

    def get_assignee(self, obj):
        return {'id': obj.assignee.id, 'email': obj.assignee.email,
                'fullname': obj.assignee.username}

    def get_reviewer(self, obj):
        return {'id': obj.reviewer.id, 'email': obj.reviewer.email,
                'fullname': obj.reviewer.username}

    class Meta:
        model = Tasks
        fields = ['id', 'board', 'title', 'description', 'status',
                  'priority', 'assignee', 'reviewer', 'assignee_id', 'reviewer_id', 'due_date']
