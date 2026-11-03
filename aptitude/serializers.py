from rest_framework import serializers
from aptitude.models import AptitudeQuestion


class AptitudeSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=500)

    option_a = serializers.CharField(max_length=200)
    option_b = serializers.CharField(max_length=200)
    option_c = serializers.CharField(max_length=200)
    option_d = serializers.CharField(max_length=200)

    correct_option = serializers.ChoiceField(
        choices=AptitudeQuestion.OPTION_CHOICES
    )
    category = serializers.ChoiceField(
        choices=AptitudeQuestion.CATEGORY_CHOICES
    )
    difficulty = serializers.ChoiceField(
        choices=AptitudeQuestion.DIFFICULTY_CHOICES
    )
    explanation = serializers.CharField()
    marks = serializers.IntegerField(min_value=1)
    is_active = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(read_only=True)



class AptitudeSubmissionSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    question_id = serializers.IntegerField()
    selected_option = serializers.ChoiceField(
        choices=AptitudeQuestion.OPTION_CHOICES
    )
    is_correct = serializers.BooleanField(read_only=True)
    points = serializers.IntegerField(
        read_only=True,
        allow_null=True
    )
    owner = serializers.CharField(max_length=100)
    remarks = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )
    submitted_at = serializers.DateTimeField(read_only=True)

    def validate(self, validated_data):
        question_id = validated_data.get('question_id')
        if not AptitudeQuestion.objects.filter(id=question_id).exists():
            raise serializers.ValidationError("Question does not exist....")
        return validated_data

    