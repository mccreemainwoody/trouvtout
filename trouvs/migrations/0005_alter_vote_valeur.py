# Generated by Django 4.1.6 on 2023-05-11 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trouvs', '0004_vote_valeur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='valeur',
            field=models.IntegerField(choices=[(1, 'Pouce bleu'), (-1, 'Pouce rouge')]),
        ),
    ]