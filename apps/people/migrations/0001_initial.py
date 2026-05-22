"""
Initial migration for the people app.
Creates all reference models and the Person model.
"""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        # ── Reference models ──────────────────────────────────────────────────

        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Gender')),
            ],
            options={'verbose_name': 'Gender', 'verbose_name_plural': 'Genders', 'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(
                    max_length=20, unique=True,
                    choices=[('junior','Junior'),('middle','Middle'),('senior','Senior'),
                             ('lead','Lead'),('head_of','Head of'),('architect','Architect')],
                    verbose_name='Level',
                )),
                ('order', models.PositiveSmallIntegerField(default=0)),
            ],
            options={'verbose_name': 'Level', 'verbose_name_plural': 'Levels', 'ordering': ['order']},
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Skill')),
            ],
            options={'verbose_name': 'Skill', 'verbose_name_plural': 'Skills', 'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='WorkingHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Working Hours')),
            ],
            options={'verbose_name': 'Working Hours', 'verbose_name_plural': 'Working Hours', 'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Region')),
            ],
            options={'verbose_name': 'Region', 'verbose_name_plural': 'Regions', 'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='WorkingPlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Working Place')),
            ],
            options={'verbose_name': 'Working Place', 'verbose_name_plural': 'Working Places', 'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='Profession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Profession')),
            ],
            options={'verbose_name': 'Profession', 'verbose_name_plural': 'Professions', 'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='English',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(
                    max_length=10, unique=True,
                    choices=[('a1','A1 — Beginner'),('a2','A2 — Elementary'),
                             ('b1','B1 — Intermediate'),('b2','B2 — Upper-Intermediate'),
                             ('c1','C1 — Advanced'),('c2','C2 — Proficient')],
                    verbose_name='English Level',
                )),
                ('order', models.PositiveSmallIntegerField(default=0)),
            ],
            options={'verbose_name': 'English Level', 'verbose_name_plural': 'English Levels', 'ordering': ['order']},
        ),

        # ── Person ────────────────────────────────────────────────────────────

        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='people/avatars/', verbose_name='Avatar')),
                ('first_name', models.CharField(max_length=150, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=150, verbose_name='Last Name')),
                ('birthdate', models.DateField(blank=True, null=True, verbose_name='Birthdate')),
                ('education', models.CharField(blank=True, max_length=255, verbose_name='Education')),
                ('work_experience', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Work Experience (years)')),
                ('salary_desired', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Salary Desired')),
                ('salary_currency', models.CharField(
                    blank=True, max_length=3, default='USD',
                    choices=[('USD','USD ($)'),('EUR','EUR (€)'),('UAH','UAH (₴)'),('RUB','RUB (₽)'),('GBP','GBP (£)')],
                    verbose_name='Currency',
                )),
                ('email', models.EmailField(blank=True, null=True, unique=True, verbose_name='E-mail')),
                ('phone', models.CharField(blank=True, max_length=50, verbose_name='Phone')),
                ('linkedin', models.URLField(blank=True, verbose_name='LinkedIn')),
                ('telegram', models.CharField(blank=True, max_length=100, verbose_name='Telegram')),
                ('status', models.CharField(
                    max_length=10, default='active',
                    choices=[('active','Active'),('inactive','Inactive')],
                    verbose_name='Status',
                )),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('cv', models.FileField(blank=True, null=True, upload_to='people/cv/', verbose_name='CV (PDF)')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                # FKs
                ('gender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='people.gender', verbose_name='Gender')),
                ('level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='people.level', verbose_name='Level')),
                ('main_skill', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='main_skill_people', to='people.skill', verbose_name='Main Skill')),
                ('english', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='people.english', verbose_name='English')),
                ('profession', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='people.profession', verbose_name='Profession')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='people.region', verbose_name='Region')),
                # M2M
                ('skills', models.ManyToManyField(blank=True, related_name='people', to='people.skill', verbose_name='Skills')),
                ('working_hours', models.ManyToManyField(blank=True, to='people.workinghours', verbose_name='Working Hours')),
                ('working_place', models.ManyToManyField(blank=True, to='people.workingplace', verbose_name='Working Place')),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'People',
                'ordering': ['last_name', 'first_name'],
                'permissions': [('export_person', 'Can export people data')],
            },
        ),
    ]
