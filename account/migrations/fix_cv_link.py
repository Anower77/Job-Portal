from django.db import migrations, models

def convert_null_to_empty_string(apps, schema_editor):
    CustomUser = apps.get_model('account', 'CustomUser')
    CustomUser.objects.filter(cv_link__isnull=True).update(cv_link='')

class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),  # Replace with your actual last migration name
    ]

    operations = [
        # First make the field nullable (if it isn't already)
        migrations.AlterField(
            model_name='customuser',
            name='cv_link',
            field=models.URLField(blank=True, null=True, max_length=500),
        ),
        # Convert null values to empty strings
        migrations.RunPython(convert_null_to_empty_string),
        # Make the field non-nullable
        migrations.AlterField(
            model_name='customuser',
            name='cv_link',
            field=models.URLField(blank=True, max_length=500, help_text="Your CV link (Google Drive or other)"),
        ),
    ] 