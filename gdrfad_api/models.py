from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=16)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    color_code = models.CharField(max_length=7)
    
    def __str__(self):
        return str(self.name)
    
class LanguageClick(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='language_click')
    created_at = models.DateField(auto_now_add=True)
    click = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.language)
    
    
class Emotion(models.Model):
    name = models.CharField(max_length=16)
    color_code = models.CharField(max_length=7)
    
    def __str__(self):
        return str(self.name)
    
    
class EmotionClick(models.Model):
    created_at = models.DateField(auto_now_add=True)
    emotion = models.ForeignKey(Emotion, on_delete=models.CASCADE, related_name='emotion_click')
    click = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.emotion)
    
    
class Service(models.Model):
    name = models.CharField(max_length=256)
    color_code = models.CharField(max_length=7)
    
    def __str__(self):
        return str(self.name)
    
    
class ServiceClick(models.Model):
    created_at = models.DateField(auto_now_add=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service_click')
    click = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.service)
    
    
class Option(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='option')
    name = models.CharField(max_length=256)
    color_code = models.CharField(max_length=7)
    
    def __str__(self):
        return str(self.name)
    
    
class OptionClick(models.Model):
    created_at = models.DateField(auto_now_add=True)
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='option_click')
    click = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.option)
    
    
class Course(models.Model):
    name = models.CharField(max_length=256)
    color_code = models.CharField(max_length=7)
    
    def __str__(self):
        return str(self.name)
    

class CourseClick(models.Model):
    created_at = models.DateField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_click')
    click = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.course)

    
class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='topic')
    name = models.CharField(max_length=256)
    color_code = models.CharField(max_length=7)
    
    def __str__(self):
        return str(self.name)
    
    
class TopicClick(models.Model):
    created_at = models.DateField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topic_click')
    click = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.topic)