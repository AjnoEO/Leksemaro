# Generated by Django 5.1.6 on 2025-03-11 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lexicon', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lexicalcategory',
            options={'verbose_name_plural': 'lexical categories'},
        ),
        migrations.AlterModelOptions(
            name='wordclass',
            options={'verbose_name_plural': 'word classes'},
        ),
        migrations.AlterField(
            model_name='lexeme',
            name='lexical_category_values',
            field=models.ManyToManyField(blank=True, to='lexicon.lexicalcategoryvalue'),
        ),
    ]
