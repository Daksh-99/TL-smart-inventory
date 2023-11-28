from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20231127_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowrecord',
            name='returned_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
