# Generated by Django 5.0 on 2024-02-29 12:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HrInterviewQuestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_list', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TechnicalInterviewQuestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_list', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=255)),
                ('is_registered', models.BooleanField(default=False)),
                ('last_three_interviews_feedback', models.TextField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, null=True)),
                ('firebase_uid', models.CharField(default='null', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('interview_id', models.AutoField(primary_key=True, serialize=False)),
                ('type_of_interview', models.CharField(choices=[('HR', 'HR'), ('Technical', 'Technical')], default='HR', max_length=10)),
                ('feedback', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.user')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField()),
                ('interview', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='base.interview')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.user')),
            ],
        ),
    ]
