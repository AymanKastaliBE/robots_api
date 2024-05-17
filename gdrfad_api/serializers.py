from rest_framework import serializers
from . import models


class LanguageClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LanguageClick
        fields = '__all__'
        

class LanguageSerializer(serializers.ModelSerializer):
    language_click = LanguageClickSerializer(many=True, read_only=True)
    class Meta:
        model = models.Language
        fields = ["name", "image", "color_code", "language_click"]
   
   
class EmotionClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmotionClick
        fields = '__all__'
        

class EmotionSerializer(serializers.ModelSerializer):
    emotion_click = EmotionClickSerializer(many=True, read_only=True)
    class Meta:
        model = models.Emotion
        fields = ["name", "color_code", "emotion_click"]
        


class OptionClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OptionClick
        fields = '__all__'
        

class OptionSerializer(serializers.ModelSerializer):
    option_click = OptionClickSerializer(many=True, read_only=True)
    class Meta:
        model = models.Option
        fields = ["service", "name", "color_code", "option_click"]


class ServiceClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceClick
        fields = '__all__'
        
     
class ServiceSerializer(serializers.ModelSerializer):
    option = OptionSerializer(many=True, read_only=True)
    service_click = ServiceClickSerializer(many=True, read_only=True)
    class Meta:
        model = models.Service
        fields = ["name", "color_code", "service_click", "option"]
        
    

class TopicClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TopicClick
        fields = '__all__'
        

class TopicSerializer(serializers.ModelSerializer):
    topic_click = TopicClickSerializer(many=True, read_only=True)
    class Meta:
        model = models.Topic
        fields = ["course", "name", "color_code", "topic_click"]


class CourseClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseClick
        fields = '__all__'
        

class CourseSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(many=True, read_only=True)
    course_click = CourseClickSerializer(many=True, read_only=True)
    class Meta:
        model = models.Course
        fields = ["id", "name", "color_code", "course_click", "topic"]