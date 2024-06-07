from datetime import datetime
from rest_framework import serializers
from . import models


class LanguageClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LanguageClick
        fields = '__all__'
        

class LanguageSerializer(serializers.ModelSerializer):
    language_click = serializers.SerializerMethodField()

    class Meta:
        model = models.Language
        fields = ["name", "image", "color_code", "language_click"]

    def get_language_click(self, obj):
        if 'start_date' in self.context and 'end_date' in self.context:
            start_date = self.context['start_date']
            end_date = self.context['end_date']
            language_click_queryset = models.LanguageClick.objects.filter(
                language=obj,
                created_at__gte=start_date,
                created_at__lte=end_date
            )
            language_click_serializer = LanguageClickSerializer(instance=language_click_queryset, many=True)
            return language_click_serializer.data
        else:
            language_click_queryset = models.LanguageClick.objects.filter(language=obj)
            language_click_serializer = LanguageClickSerializer(instance=language_click_queryset, many=True)
            return language_click_serializer.data
        
   
   
class EmotionClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmotionClick
        fields = '__all__'
        

class EmotionSerializer(serializers.ModelSerializer):
    # emotion_click = EmotionClickSerializer(many=True, read_only=True)
    emotion_click = serializers.SerializerMethodField()

    class Meta:
        model = models.Emotion
        fields = ["name", "color_code", "emotion_click"]
        
    def get_emotion_click(self, obj):
        if 'start_date' in self.context and 'end_date' in self.context:
            start_date = self.context['start_date']
            end_date = self.context['end_date']
            emotion_click_queryset = models.EmotionClick.objects.filter(
                emotion=obj,
                created_at__gte=start_date,
                created_at__lte=end_date
            )
            emotion_click_serializer = EmotionClickSerializer(instance=emotion_click_queryset, many=True)
            return emotion_click_serializer.data
        else:
            emotion_click_queryset = models.EmotionClick.objects.filter(emotion=obj)
            emotion_click_serializer = EmotionClickSerializer(instance=emotion_click_queryset, many=True)
            return emotion_click_serializer.data
        


class OptionClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OptionClick
        fields = '__all__'
        

class OptionSerializer(serializers.ModelSerializer):
    # option_click = OptionClickSerializer(many=True, read_only=True)
    option_click = serializers.SerializerMethodField()
    class Meta:
        model = models.Option
        fields = ["service", "name", "color_code", "option_click"]
        
    def get_option_click(self, obj):
        if 'start_date' in self.context and 'end_date' in self.context:
            start_date = self.context['start_date']
            end_date = self.context['end_date']
            option_click_queryset = models.OptionClick.objects.filter(
                option=obj,
                created_at__gte=start_date,
                created_at__lte=end_date
            )
            option_click_serializer = OptionClickSerializer(instance=option_click_queryset, many=True)
            return option_click_serializer.data
        else:
            option_click_queryset = models.OptionClick.objects.filter(option=obj)
            option_click_serializer = OptionClickSerializer(instance=option_click_queryset, many=True)
            return option_click_serializer.data


class ServiceClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceClick
        fields = '__all__'
        
     
class ServiceSerializer(serializers.ModelSerializer):
    option = OptionSerializer(many=True, read_only=True)
    # service_click = ServiceClickSerializer(many=True, read_only=True)
    service_click = serializers.SerializerMethodField()
    class Meta:
        model = models.Service
        fields = ["name", "color_code", "service_click", "option"]
          
    def get_service_click(self, obj):
        if 'start_date' in self.context and 'end_date' in self.context:
            start_date = self.context['start_date']
            end_date = self.context['end_date']
            service_click_queryset = models.ServiceClick.objects.filter(
                service=obj,
                created_at__gte=start_date,
                created_at__lte=end_date
            )
            service_click_serializer = ServiceClickSerializer(instance=service_click_queryset, many=True)
            return service_click_serializer.data
        else:
            service_click_queryset = models.ServiceClick.objects.filter(service=obj)
            service_click_serializer = ServiceClickSerializer(instance=service_click_queryset, many=True)
            return service_click_serializer.data


class TopicClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TopicClick
        fields = '__all__'
        

class TopicSerializer(serializers.ModelSerializer):
    # topic_click = TopicClickSerializer(many=True, read_only=True)
    topic_click = serializers.SerializerMethodField()
    class Meta:
        model = models.Topic
        fields = ["course", "name", "color_code", "topic_click"]
        
    def get_topic_click(self, obj):
        if 'start_date' in self.context and 'end_date' in self.context:
            start_date = self.context['start_date']
            end_date = self.context['end_date']
            topic_click_queryset = models.TopicClick.objects.filter(
                topic=obj,
                created_at__gte=start_date,
                created_at__lte=end_date
            )
            topic_click_serializer = TopicClickSerializer(instance=topic_click_queryset, many=True)
            return topic_click_serializer.data
        else:
            topic_click_queryset = models.TopicClick.objects.filter(topic=obj)
            topic_click_serializer = TopicClickSerializer(instance=topic_click_queryset, many=True)
            return topic_click_serializer.data


class CourseClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseClick
        fields = '__all__'
        

class CourseSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(many=True, read_only=True)
    # course_click = CourseClickSerializer(many=True, read_only=True)
    course_click = serializers.SerializerMethodField()
    class Meta:
        model = models.Course
        fields = ["id", "name", "color_code", "course_click", "topic"]

    def get_course_click(self, obj):
        if 'start_date' in self.context and 'end_date' in self.context:
            start_date = self.context['start_date']
            end_date = self.context['end_date']
            course_click_queryset = models.CourseClick.objects.filter(
                course=obj,
                created_at__gte=start_date,
                created_at__lte=end_date
            )
            course_click_serializer = CourseClickSerializer(instance=course_click_queryset, many=True)
            return course_click_serializer.data
        else:
            course_click_queryset = models.CourseClick.objects.filter(course=obj)
            course_click_serializer = CourseClickSerializer(instance=course_click_queryset, many=True)
            return course_click_serializer.data