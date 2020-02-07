# Generated by Django 2.2.7 on 2019-11-18 19:41


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('abbreviation', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='AssetClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_price', models.DecimalField(decimal_places=20, max_digits=50)),
                ('close_price', models.DecimalField(decimal_places=20, max_digits=50)),
                ('high_price', models.DecimalField(decimal_places=20, max_digits=50)),
                ('low_price', models.DecimalField(decimal_places=20, max_digits=50)),
                ('date', models.DateField()),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfolio.Asset')),
            ],
        ),
        migrations.AddField(
            model_name='asset',
            name='asset_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfolio.AssetClass'),
        ),
    ]