from django.db import migrations, models
import django.db.models.deletion


def person_file_upload_to(instance, filename):
    """Store files under people/<person_pk>/filename."""
    return f'people/{instance.person_id}/{filename}'


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [

        migrations.RemoveField(
            model_name='person',
            name='cv',
        ),

        migrations.CreateModel(
            name='PersonFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('file', models.FileField(
                    upload_to=person_file_upload_to,
                    verbose_name='File',
                )),
                ('file_type', models.CharField(
                    choices=[
                        ('cv',        'CV / Résumé'),
                        ('portfolio', 'Portfolio'),
                        ('test',      'Test Task'),
                        ('other',     'Other'),
                    ],
                    default='cv',
                    max_length=20,
                    verbose_name='File Type',
                )),
                ('description', models.CharField(
                    blank=True, max_length=255, verbose_name='Description',
                )),
                ('uploaded_at', models.DateTimeField(
                    auto_now_add=True, verbose_name='Uploaded At',
                )),
                ('person', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='files',
                    to='people.person',
                    verbose_name='Person',
                )),
            ],
            options={
                'verbose_name':        'Person File',
                'verbose_name_plural': 'Person Files',
                'ordering':            ['-uploaded_at'],
            },
        ),
    ]