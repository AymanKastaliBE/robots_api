# Generated by Django 4.2 on 2024-05-07 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gdrfad_api', '0004_topicclick_serviceclick_optionclick_courseclick'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseclick',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_click', to='gdrfad_api.course'),
        ),
        migrations.AlterField(
            model_name='emotionclick',
            name='emotion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emotion_click', to='gdrfad_api.emotion'),
        ),
        migrations.AlterField(
            model_name='languageclick',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='language_click', to='gdrfad_api.language'),
        ),
        migrations.AlterField(
            model_name='option',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='option', to='gdrfad_api.service'),
        ),
        migrations.AlterField(
            model_name='optionclick',
            name='option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='option_click', to='gdrfad_api.option'),
        ),
        migrations.AlterField(
            model_name='serviceclick',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_click', to='gdrfad_api.service'),
        ),
        migrations.AlterField(
            model_name='topicclick',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic_click', to='gdrfad_api.topic'),
        ),
    ]
