from rest_framework import serializers
from boards_app.models import Boards
from django.contrib.auth.models import User
from ..models import Tasks, Comments


class PostTaskSerializer(serializers.ModelSerializer):
    board = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Boards.objects.all(),
        required=True
    )

    assignee_id = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=User.objects.all(),
        required=False,
        write_only=True,
        source='assignee'
    )
    assignee = serializers.SerializerMethodField()

    reviewer_id = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=User.objects.all(),
        required=False,
        write_only=True,
        source='reviewer'
    )

    reviewer = serializers.SerializerMethodField()

    comments_count = serializers.SerializerMethodField()

    def get_assignee(self, obj):
        if obj.assignee == None:
            return
        return {'id': obj.assignee.id, 'email': obj.assignee.email,
                'fullname': obj.assignee.username}

    def get_reviewer(self, obj):
        if obj.reviewer == None:
            return
        return {'id': obj.reviewer.id, 'email': obj.reviewer.email,
                'fullname': obj.reviewer.username}

    def get_comments_count(self, obj):
        return obj.comment.count()

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
        if obj.assignee == None:
            return
        return {'id': obj.assignee.id, 'email': obj.assignee.email,
                'fullname': obj.assignee.username}

    def get_reviewer(self, obj):
        if obj.reviewer == None:
            return
        return {'id': obj.reviewer.id, 'email': obj.reviewer.email,
                'fullname': obj.reviewer.username}

    class Meta:
        model = Tasks
        fields = ['id', 'board', 'title', 'description', 'status',
                  'priority', 'assignee', 'reviewer', 'assignee_id', 'reviewer_id', 'due_date']


class AssignedToMeOrReviewerSerializer(serializers.ModelSerializer):
    assignee = serializers.SerializerMethodField()
    reviewer = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    def get_assignee(self, obj):
        if obj.assignee == None:
            return
        return {'id': obj.assignee.id, 'email': obj.assignee.email, 'fullname': obj.assignee.username}

    def get_reviewer(self, obj):
        if obj.reviewer == None:
            return
        return {'id': obj.reviewer.id, 'email': obj.reviewer.email, 'fullname': obj.reviewer.username}

    def get_comments_count(self, obj):
        return obj.comment.count()

    class Meta:
        model = Tasks
        fields = [
            'id', 'board', 'title', 'description', 'status', 'priority', 'assignee', 'reviewer', 'due_date', 'comments_count'
        ]


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%SZ", read_only=True)

    def get_author(self, obj):
        if obj.author == None:
            return
        return obj.author.username

    class Meta:
        model = Comments
        fields = ['id', 'created_at', 'author', 'content']
