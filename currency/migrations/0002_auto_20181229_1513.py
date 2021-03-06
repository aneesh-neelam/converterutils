# Generated by Django 2.1.4 on 2018-12-29 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConversionRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exchange_rate', models.FloatField(default=1.0)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('base_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversionrate_base_currency', to='currency.Currency')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversionrate_currency', to='currency.Currency')),
            ],
        ),
        migrations.RemoveField(
            model_name='conversionrates',
            name='base_currency',
        ),
        migrations.RemoveField(
            model_name='conversionrates',
            name='currency',
        ),
        migrations.DeleteModel(
            name='ConversionRates',
        ),
    ]
