# Generated by Django 3.1.2 on 2020-10-14 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Matches',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('season', models.IntegerField(default=0)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('team1', models.CharField(blank=True, max_length=50, null=True)),
                ('team2', models.CharField(blank=True, max_length=50, null=True)),
                ('toss_winner', models.CharField(blank=True, max_length=50, null=True)),
                ('toss_decision', models.CharField(blank=True, max_length=50, null=True)),
                ('result', models.CharField(blank=True, max_length=50, null=True)),
                ('dl_applied', models.BooleanField(default=False)),
                ('winner', models.CharField(blank=True, max_length=50, null=True)),
                ('win_by_runs', models.IntegerField(default=0)),
                ('win_by_wickets', models.IntegerField(default=0)),
                ('player_of_match', models.CharField(blank=True, max_length=50, null=True)),
                ('venue', models.CharField(blank=True, max_length=100, null=True)),
                ('umpire1', models.CharField(blank=True, max_length=50, null=True)),
                ('umpire2', models.CharField(blank=True, max_length=50, null=True)),
                ('umpire3', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'Matches',
            },
        ),
        migrations.CreateModel(
            name='Deliveries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inning', models.IntegerField(default=0)),
                ('batting_team', models.CharField(blank=True, max_length=50, null=True)),
                ('bowling_team', models.CharField(blank=True, max_length=50, null=True)),
                ('over', models.IntegerField(default=0)),
                ('ball', models.IntegerField(default=0)),
                ('batsman', models.CharField(blank=True, max_length=50, null=True)),
                ('non_striker', models.CharField(blank=True, max_length=50, null=True)),
                ('bowler', models.CharField(blank=True, max_length=50, null=True)),
                ('is_super_over', models.IntegerField(default=0)),
                ('wide_runs', models.IntegerField(default=0)),
                ('bye_runs', models.IntegerField(default=0)),
                ('legbye_runs', models.IntegerField(default=0)),
                ('noball_runs', models.IntegerField(default=0)),
                ('penalty_runs', models.IntegerField(default=0)),
                ('batsman_runs', models.IntegerField(default=0)),
                ('extra_runs', models.IntegerField(default=0)),
                ('total_runs', models.IntegerField(default=0)),
                ('player_dismissed', models.CharField(blank=True, max_length=50, null=True)),
                ('dismissal_kind', models.CharField(blank=True, max_length=50, null=True)),
                ('fielder', models.CharField(blank=True, max_length=50, null=True)),
                ('match_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='GALEApp.matches')),
            ],
            options={
                'db_table': 'Deliveries',
            },
        ),
    ]
