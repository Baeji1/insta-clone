# Generated by Django 2.0.6 on 2018-11-14 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionmodel',
            name='post_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insta.Post'),
        ),
        migrations.AlterField(
            model_name='actionmodel',
            name='uid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insta.UserModel'),
        ),
        migrations.AlterField(
            model_name='commentmodel',
            name='c_parent_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='insta.CommentModel'),
        ),
        migrations.AlterField(
            model_name='commentmodel',
            name='c_post_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insta.Post'),
        ),
        migrations.AlterField(
            model_name='commentmodel',
            name='c_uid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insta.UserModel'),
        ),
        migrations.AlterField(
            model_name='followmodel',
            name='a_username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insta.UserModel'),
        ),
        migrations.AlterField(
            model_name='post',
            name='uid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insta.UserModel'),
        ),
    ]