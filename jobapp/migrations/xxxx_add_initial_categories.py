from django.db import migrations

def add_initial_categories(apps, schema_editor):
    Category = apps.get_model('jobapp', 'Category')
    categories = [
        'Technology',
        'Healthcare',
        'Education',
        'Finance',
        'Marketing',
        'Sales',
        'Design',
        'Engineering',
        'Customer Service',
        'Other'
    ]
    for category_name in categories:
        Category.objects.create(name=category_name)

class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0001_initial'),  # Replace with your last migration
    ]

    operations = [
        migrations.RunPython(add_initial_categories),
    ] 