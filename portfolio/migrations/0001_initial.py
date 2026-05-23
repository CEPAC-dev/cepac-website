# Generated migration file for portfolio app

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Project Category',
                'verbose_name_plural': 'Project Categories',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='portfolio/%Y/%m/')),
                ('description', models.CharField(help_text='Short description shown on card', max_length=200)),
                ('about', models.TextField(help_text='About the project - full content')),
                ('location', models.CharField(max_length=255)),
                ('services', models.TextField(help_text='Services offered (one per line)')),
                ('software_tools', models.TextField(help_text='Software & Tools used (one per line)')),
                ('key_elements', models.TextField(blank=True, help_text='Key Study Elements (one per line)', null=True)),
                ('statistical_analysis', models.TextField(blank=True, help_text='Statistical & Technical Analysis (one per line)', null=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects', to='portfolio.projectcategory')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
                'ordering': ['order', '-created_at'],
            },
        ),
    ]
