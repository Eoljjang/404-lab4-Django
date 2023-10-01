from rest_framework import serializers
from .models import Question

# "model" = Question => In this example.

class QuestionSerializer(serializers.Serializer):
    # 1) What you want to serialize
    question_text = serializers.CharField() 
    pub_date = serializers.DateTimeField()

    # 2) Create & return a new "model" instance, given the validated data.
    def create(self, validated_data):
        return Question.object.create(**validated_data)
    
    # 3) Update & return an existing "modeL" instance, given the validated data.
    def update(self, instance, validated_data):
        instance.question_text = validated_data.get("question_text", instance.question_text)
        instance.pub_date = validated_data.get("pub_date", instance.pub_date)
        instance.save()
        return instance
