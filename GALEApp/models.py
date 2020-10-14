from django.db import models

# Create your models here.

class Matches(models.Model):
    id = models.IntegerField(primary_key=True, editable=True)
    season = models.IntegerField(default=0)
    city = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    team1 = models.CharField(max_length=50, null=True, blank=True)
    team2 = models.CharField(max_length=50, null=True, blank=True)
    toss_winner = models.CharField(max_length=50, null=True, blank=True)
    toss_decision = models.CharField(max_length=50, null=True, blank=True)
    result = models.CharField(max_length=50, null=True, blank=True)
    dl_applied = models.BooleanField(default=False)
    winner = models.CharField(max_length=50, null=True, blank=True)
    win_by_runs = models.IntegerField(default=0)
    win_by_wickets = models.IntegerField(default=0)
    player_of_match = models.CharField(max_length=50, null=True, blank=True)
    venue = models.CharField(max_length=100, null=True, blank=True)
    umpire1 = models.CharField(max_length=50, null=True, blank=True)
    umpire2 = models.CharField(max_length=50, null=True, blank=True)
    umpire3 = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "Matches"


class Deliveries(models.Model):
    match = models.ForeignKey(Matches, on_delete=models.CASCADE, null=True, blank=True)
    inning = models.IntegerField(default=0)
    batting_team = models.CharField(max_length=50, null=True, blank=True)
    bowling_team = models.CharField(max_length=50, null=True, blank=True)
    over = models.IntegerField(default=0)
    ball = models.IntegerField(default=0)
    batsman = models.CharField(max_length=50, null=True, blank=True)
    non_striker = models.CharField(max_length=50, null=True, blank=True)
    bowler = models.CharField(max_length=50, null=True, blank=True)
    is_super_over = models.IntegerField(default=0)
    wide_runs = models.IntegerField(default=0)
    bye_runs = models.IntegerField(default=0)
    legbye_runs = models.IntegerField(default=0)
    noball_runs = models.IntegerField(default=0)
    penalty_runs = models.IntegerField(default=0)
    batsman_runs = models.IntegerField(default=0)
    extra_runs = models.IntegerField(default=0)
    total_runs = models.IntegerField(default=0)
    player_dismissed = models.CharField(max_length=50, null=True, blank=True)
    dismissal_kind = models.CharField(max_length=50, null=True, blank=True)
    fielder = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "Deliveries"

