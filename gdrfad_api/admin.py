from django.contrib import admin
from . import models


class LanguageAdmin(admin.ModelAdmin):
    list_display = ["name", "image", "color_code"]

admin.site.register(models.Language, LanguageAdmin)


class LanguageClickAdmin(admin.ModelAdmin):
    list_display = ["created_at", "language", "click"]

admin.site.register(models.LanguageClick, LanguageClickAdmin)


class EmotionAdmin(admin.ModelAdmin):
    list_display = ["name", "color_code"]

admin.site.register(models.Emotion, EmotionAdmin)


class EmotionClickAdmin(admin.ModelAdmin):
    list_display = ["created_at", "emotion", "click"]

admin.site.register(models.EmotionClick, EmotionClickAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "color_code"]

admin.site.register(models.Service, ServiceAdmin)


class ServiceClickAdmin(admin.ModelAdmin):
    list_display = ["created_at", "service", "click"]

admin.site.register(models.ServiceClick, ServiceClickAdmin)


class OptionAdmin(admin.ModelAdmin):
    list_display = ["service", "name", "color_code"]

admin.site.register(models.Option, OptionAdmin)


class OptionClickAdmin(admin.ModelAdmin):
    list_display = ["created_at", "option", "click"]

admin.site.register(models.OptionClick, OptionClickAdmin)


class CourseAdmin(admin.ModelAdmin):
    list_display = ["name", "color_code"]

admin.site.register(models.Course, CourseAdmin)


class CourseClickAdmin(admin.ModelAdmin):
    list_display = ["created_at", "course", "click"]

admin.site.register(models.CourseClick, CourseClickAdmin)


class TopicAdmin(admin.ModelAdmin):
    list_display = ["course", "name", "color_code"]

admin.site.register(models.Topic, TopicAdmin)


class TopicClickAdmin(admin.ModelAdmin):
    list_display = ["created_at", "topic", "click"]

admin.site.register(models.TopicClick, TopicClickAdmin)
