from datetime import datetime
import logging
import os

from django.conf import settings
from django.db.models import Count

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib import messages
import re
from django.template.response import TemplateResponse
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import F
from django.db.models import Sum


# Create your views here.

def home(request):
    seasons = Matches.objects.values_list('season', flat=True).order_by('-season').distinct()
    context = {
        'seasons': seasons,
        'template': 'home'
    }
    return render(request, 'base.html', context)
       

def get_season_data(request, season):
    season = int(season)
    seasons = Matches.objects.values_list('season', flat=True).order_by('-season').distinct()

    dataList = []
    default_items = []
    labels = []
    if season > 0:
        matches = Matches.objects.filter(season=season)
        # top 4 teams in terms of wins..
        teams = matches.values('winner') \
                       .annotate(wins_count=Count('winner')) \
                       .order_by('-wins_count')[:4]

        for team in teams:
            labels.append(team['winner'])
            default_items.append(team['wins_count'])

        top_4_teams = {
            'labels': labels,
            'defaults': default_items
        }

        # most number of tosses wins..
        tosses = matches.values('toss_winner').annotate(toss_wins_count=Count('toss_winner')) \
                       .order_by('-toss_wins_count').first()

        # there could be more than one team winning the most number of tosses..
        max_tosses_count = tosses['toss_wins_count']
        tosses = matches.values('toss_winner').annotate(toss_wins_count=Count('toss_winner')) \
                       .filter(toss_wins_count=max_tosses_count) \
                       .order_by('-toss_wins_count')
        

        
        # most number of player of the match awards..
        most_awards = matches.values('player_of_match').annotate(player_of_match_wins_count=Count('player_of_match')) \
                       .order_by('-player_of_match_wins_count').first()
        
        most_mom = most_awards['player_of_match_wins_count']
        most_awards = matches.values('player_of_match').annotate(player_of_match_wins_count=Count('player_of_match')) \
                       .filter(player_of_match_wins_count=most_mom) \
                       .order_by('-player_of_match_wins_count')



        # max wins by team.
        wins = matches.values('winner') \
                       .annotate(wins_count=Count('winner')) \
                       .order_by('-wins_count').first()

        most_wins = wins['wins_count']
        wins = matches.values('winner') \
                       .annotate(wins_count=Count('winner')) \
                       .filter(wins_count=most_wins) \
                       .order_by('-wins_count')


        #Which location has the most number of wins for the top team
        # find out the team which has max wins..
        teams = []
        for r in wins:
            teams.append(r['winner'])
        #team = wins['winner']
        # now find out the location which has most wins for this team..
        venue = matches.filter(winner__in=list(teams)).values('venue', 'winner') \
                       .annotate(wins_count=Count('venue')) \
                       .order_by('-wins_count').first()

        # Which % of teams decided to bat when they won the toss
        # get total number of matches for the season..
        total_matches = matches.count()
        number_of_teams_batted_first = matches.filter(toss_decision='bat').count()

        if total_matches > 0:
            team_percenatge = (number_of_teams_batted_first/total_matches) * 100
        else:
            team_percenatge = 0
                    
        # Which location hosted most number of matches and win % and loss % for the season
        # THIS IS FOR THE MOST NUMBER OF WINNING TEAM
        # find out location which hosted most matches..
        most_matches_by_location = matches.values('venue') \
                       .annotate(matches_count=Count('venue')) \
                       .order_by('-matches_count')[:1]

        location = None
        matches_count = 0
        for r in most_matches_by_location:
            location = r['venue']
            matches_count = r['matches_count']
        matches_won_at_location = matches.values()

        # Which team won by the highest margin of runs  for the season
        win_by_heighest_runs = matches.filter(win_by_runs__gt=0) \
                        .values('winner', 'win_by_runs') \
                        .order_by('-win_by_runs').first()

        heighest_margin_by_run = win_by_heighest_runs['win_by_runs']

        win_by_heighest_runs = matches.filter(win_by_runs__gt=0) \
                        .values('winner', 'win_by_runs') \
                        .filter(win_by_runs=heighest_margin_by_run) \
                        .order_by('-win_by_runs')
        
        # Which team won by the highest number of wickets for the season
        win_by_heighest_wkts = matches.filter(win_by_wickets__gt=0) \
                        .values('winner', 'win_by_wickets') \
                        .order_by('-win_by_wickets').first()

        highest_wkt_margin = win_by_heighest_wkts['win_by_wickets']

        win_by_heighest_wkts = matches.filter(win_by_wickets__gt=0) \
                        .values('winner', 'win_by_wickets') \
                        .filter(win_by_wickets=highest_wkt_margin) \
                        .order_by('-win_by_wickets')


        # How many times has a team won the toss and the match
        teams_won_toss_and_match = matches.filter(toss_winner=F('winner')).count()


        # Which Batsman (or bowler?) gave away the most number of runs in a match for the selected season
        # get match IDs for the season..
        match_ids = matches.values_list('id', flat=True).distinct()

        #print(match_ids)
        #most_runs_given_by_bowler = Deliveries.objects.filter(match_id__in=list(match_ids)) \
        #                            .annotate(runs_given=sum('total_runs')) \
        #                            .order_by('-runs_given').first()

        #print(most_runs_given_by_bowler)

        # Most number of catches by a fielder in a match for the selected season

        dataList = {
            'tosses': tosses,
            'most_awards': most_awards,
            'wins': wins,
            'venue': venue,
            'team_percenatge': team_percenatge,
            'win_by_heighest_runs': win_by_heighest_runs,
            'win_by_heighest_wkts': win_by_heighest_wkts,
            'teams_won_toss_and_match': teams_won_toss_and_match,
            'top_4_teams': top_4_teams
        }

        context = {
            'seasons': seasons,
            'dataList': dataList,
            'template': 'home',
            'selectedSeason': season
        }
    return render(request, 'base.html', context)




