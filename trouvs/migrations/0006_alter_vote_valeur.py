# Generated by Django 4.1.6 on 2023-05-11 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trouvs', '0005_alter_vote_valeur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='valeur',
            field=models.IntegerField(choices=[(1, 'Pouce Bleu'), (-1, 'Pouce Rouge')]),
        ),
    ]
