# Generated by Django 4.2.7 on 2023-12-16 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mudryk', '0009_course_textwithlistforcourse_textforcourse_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listitemfortext',
            name='list_item_for_text_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='list_item_for_text', to='mudryk.textwithlistforcourse'),
        ),
    ]
