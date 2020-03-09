# Generated by Django 3.0.3 on 2020-03-08 04:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Post', '0005_auto_20200308_0745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='type_post',
            field=models.CharField(choices=[('S', 'ขาย'), ('B', 'ซื้อ')], max_length=1),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('create_date', models.DateField(auto_now=True)),
                ('create_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Post.Book')),
            ],
        ),
    ]