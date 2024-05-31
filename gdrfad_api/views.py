from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from . import models, serializers
from auth_api.decorators import login_required
from django.utils.decorators import method_decorator
import pandas as pd
from rest_framework import  authentication
from auth_api.permissions import StaffOnly, GDRFADOnly
from django.utils.text import slugify


class DashboardView(APIView):
    template_name = 'gdrfad_api/dashboard.html'
    permission_classes = [StaffOnly or GDRFADOnly]

    @classmethod
    def get_excel_filename(cls, start_date, end_date):
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        filename = f"dashboard_report_from_{start_date_str}_to_{end_date_str}.xlsx"
        # Remove any characters that are not allowed in filenames
        return slugify(filename)

    @method_decorator(login_required, name='dispatch')
    def get(self, request, format=None, *args, **kwargs):
        context = {}
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        action = request.GET.get('action', 'show_data')
        if start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            
            languages = models.Language.objects.filter(language_click__created_at__range=[start_date, end_date]).distinct()
            emotions = models.Emotion.objects.filter(emotion_click__created_at__range=[start_date, end_date]).distinct()
            services = models.Service.objects.filter(service_click__created_at__range=[start_date, end_date]).distinct()
            courses = models.Course.objects.filter(course_click__created_at__range=[start_date, end_date]).distinct()
        else:
            languages = models.Language.objects.all()
            emotions = models.Emotion.objects.all()
            services = models.Service.objects.all()
            courses = models.Course.objects.all()
            
        language_serializer = serializers.LanguageSerializer(languages, many=True)
        emotion_serializer = serializers.EmotionSerializer(emotions, many=True)
        service_serializer = serializers.ServiceSerializer(services, many=True)
        course_serializer = serializers.CourseSerializer(courses, many=True)
        
        context['language_serializer'] = language_serializer.data
        context['emotion_serializer'] = emotion_serializer.data
        context['service_serializer'] = service_serializer.data
        context['course_serializer'] = course_serializer.data

        if format == 'json':
            return Response(context)
        elif action == 'download_report':
            # Generate Excel report and return response
            excel_filename = self.get_excel_filename(start_date, end_date)
            excel_file_response = self.generate_excel_report(context, excel_filename)
            return excel_file_response
        else:
            return render(request, template_name=self.template_name, context=context)


    def generate_excel_report(self, context, filename):
        # Extract the main keys
        main_keys = list(context.keys())

        # Create an empty dictionary to hold DataFrames for each key
        data_frames = {}

        # Populate DataFrames for each main key
        for key in main_keys:
            data = context[key]
            # Extract the 'name' and 'click' fields for each item in the list
            names = [item.get('name', '') for item in data]
            clicks = [sum(click_dict.get('click', 0) for click_dict in item.get('{}_click'.format(key.split('_')[0]), [])) for item in data]

            # Create a DataFrame with these names and clicks
            df = pd.DataFrame({
                f"{key.split('_')[0]}s": names,
                f"{key.split('_')[0]}s clicks": clicks
            })

            if key == 'course_serializer':
                # Handle topics for courses
                topics_data = []
                for item in data:
                    course_name = item.get('name', '')
                    topics = item.get('topic', [])
                    for topic in topics:
                        topics_data.append({
                            'course': course_name,
                            'topic_name': topic.get('name', ''),
                            'topic_clicks': sum(click_dict.get('click', 0) for click_dict in topic.get('topic_click', []))
                        })

                topics_df = pd.DataFrame(topics_data)
                data_frames['courses topic'] = topics_df
                
            elif key == 'service_serializer':
                # Handle options for services
                options_data = []
                for item in data:
                    service_name = item.get('name', '')
                    options = item.get('option', [])
                    for option in options:
                        options_data.append({
                            'service': service_name,
                            'option_name': option.get('name', ''),
                            'option_clicks': sum(click_dict.get('click', 0) for click_dict in option.get('option_click', []))
                        })

                options_df = pd.DataFrame(options_data)
                data_frames['services option'] = options_df

            data_frames[key] = df

        # Create a Pandas Excel writer using ExcelWriter
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={filename}.xlsx'
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            # Write each DataFrame to a separate sheet
            for key, df in data_frames.items():
                df.to_excel(writer, index=False, sheet_name=f"{key.split('_')[0]}s")

        return response

dashboard_view = DashboardView.as_view()


# class DashboardView(APIView):
#     template_name = 'gdrfad_api/dashboard.html'
#     permission_classes = [StaffOnly or GDRFADOnly]

#     @method_decorator(login_required, name='dispatch')
#     def get(self, request, format=None, *args, **kwargs):
#         context = {}
#         start_date = request.query_params.get('start_date')
#         end_date = request.query_params.get('end_date')
#         action = request.GET.get('action', 'show_data')
#         if start_date and end_date:
#             start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
#             end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            
#             languages = models.Language.objects.filter(language_click__created_at__range=[start_date, end_date]).distinct()
#             emotions = models.Emotion.objects.filter(emotion_click__created_at__range=[start_date, end_date]).distinct()
#             services = models.Service.objects.filter(service_click__created_at__range=[start_date, end_date]).distinct()
#             courses = models.Course.objects.filter(course_click__created_at__range=[start_date, end_date]).distinct()
#         else:
#             languages = models.Language.objects.all()
#             emotions = models.Emotion.objects.all()
#             services = models.Service.objects.all()
#             courses = models.Course.objects.all()
            
#         language_serializer = serializers.LanguageSerializer(languages, many=True)
#         emotion_serializer = serializers.EmotionSerializer(emotions, many=True)
#         service_serializer = serializers.ServiceSerializer(services, many=True)
#         course_serializer = serializers.CourseSerializer(courses, many=True)
        
#         context['language_serializer'] = language_serializer.data
#         context['emotion_serializer'] = emotion_serializer.data
#         context['service_serializer'] = service_serializer.data
#         context['course_serializer'] = course_serializer.data

#         if format == 'json':
#             return Response(context)
#         elif action == 'download_report':
#             # Generate Excel report and return response
#             excel_file_response = self.generate_excel_report(context)
#             return excel_file_response
#         else:
#             return render(request, template_name=self.template_name, context=context)


#     def generate_excel_report(self, context):
#         # Extract the main keys
#         main_keys = list(context.keys())

#         # Create an empty dictionary to hold DataFrames for each key
#         data_frames = {}

#         # Populate DataFrames for each main key
#         for key in main_keys:
#             data = context[key]
#             # Extract the 'name' and 'click' fields for each item in the list
#             names = [item.get('name', '') for item in data]
#             clicks = [sum(click_dict.get('click', 0) for click_dict in item.get('{}_click'.format(key.split('_')[0]), [])) for item in data]

#             # Create a DataFrame with these names and clicks
#             df = pd.DataFrame({
#                 f"{key.split('_')[0]}s": names,
#                 f"{key.split('_')[0]}s clicks": clicks
#             })

#             if key == 'course_serializer':
#                 # Handle topics for courses
#                 topics_data = []
#                 for item in data:
#                     course_name = item.get('name', '')
#                     topics = item.get('topic', [])
#                     for topic in topics:
#                         topics_data.append({
#                             'course': course_name,
#                             'topic_name': topic.get('name', ''),
#                             'topic_clicks': sum(click_dict.get('click', 0) for click_dict in topic.get('topic_click', []))
#                         })

#                 topics_df = pd.DataFrame(topics_data)
#                 data_frames['courses topic'] = topics_df
                
#             elif key == 'service_serializer':
#                 # Handle options for services
#                 options_data = []
#                 for item in data:
#                     service_name = item.get('name', '')
#                     options = item.get('option', [])
#                     for option in options:
#                         options_data.append({
#                             'service': service_name,
#                             'option_name': option.get('name', ''),
#                             'option_clicks': sum(click_dict.get('click', 0) for click_dict in option.get('option_click', []))
#                         })

#                 options_df = pd.DataFrame(options_data)
#                 data_frames['services option'] = options_df

#             data_frames[key] = df

#         # Create a Pandas Excel writer using ExcelWriter
#         response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#         response['Content-Disposition'] = 'attachment; filename=dashboard_report.xlsx'
#         with pd.ExcelWriter(response, engine='openpyxl') as writer:
#             # Write each DataFrame to a separate sheet
#             for key, df in data_frames.items():
#                 df.to_excel(writer, index=False, sheet_name=f"{key.split('_')[0]}s")

#         return response

# dashboard_view = DashboardView.as_view()


class IncrementRobotOptions(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [AllowAny]
    
    def patch(self, request, *args, **kwargs):
        
        key = request.data.get('key')
        value = request.data.get('value')
            
        if key == 'service':
            service = get_object_or_404(models.Service, name=value)
            service_click = get_object_or_404(models.ServiceClick, service=service)
            service_click.click += 1
            service_click.save()
        if key == 'option':
            option = get_object_or_404(models.Option, name=value)
            option_click = get_object_or_404(models.OptionClick, option=option)
            option_click.click += 1
            option_click.save()
        if key == 'course':
            course = get_object_or_404(models.Course, name=value)
            course_click = get_object_or_404(models.CourseClick, course=course)
            course_click.click += 1
            course_click.save()
        if key == 'topic':
            topic = get_object_or_404(models.Topic, name=value)
            topic_click = get_object_or_404(models.TopicClick, topic=topic)
            topic_click.click += 1
            topic_click.save()
        if key == 'emotion':
            emotion = get_object_or_404(models.Emotion, name=value)
            emotion_click = get_object_or_404(models.EmotionClick, emotion=emotion)
            emotion_click.click += 1
            emotion_click.save()
        if key == 'language':
            language = get_object_or_404(models.Language, name=value)
            language_click = get_object_or_404(models.LanguageClick, language=language)
            language_click.click += 1
            language_click.save()
    
        return Response({"message": "patch working"})
    
    
increment_robot_options_view = IncrementRobotOptions.as_view()