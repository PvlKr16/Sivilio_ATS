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
                    verbose_name='CV (PDF)',
                    help_text='PDF files only',
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
