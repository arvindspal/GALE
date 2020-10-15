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



        #Which location hosted most number of matches and win % and loss % for the season
        most_matches_by_locations = matches.values('venue') \
                       .annotate(matches_count=Count('venue')) \
                       .order_by('-matches_count').first()

        most_match_count = most_matches_by_locations['matches_count']

        most_matches_by_locations = matches.values('venue') \
                       .annotate(matches_count=Count('venue')) \
                       .filter(matches_count=most_match_count) \
                       .order_by('-matches_count')


        # Which Batsman (or bowler?) gave away the most number of runs in a match for the selected season
        # get match IDs for the season..
        match_ids = matches.values_list('id', flat=True).distinct()

        bowler_with_most_runs = []
        max_runs = 0
        #print(match_ids)
        for match_id in match_ids:
            deliveries = Deliveries.objects.filter(match_id=match_id)
            # now group this by bowler..
            bowler = deliveries.values('bowler') \
                                .annotate(total_runs_given=Sum('total_runs')) \
                                .order_by('-total_runs_given').first()

            if bowler['total_runs_given'] > max_runs:
                # get the match..
                match = Matches.objects.get(id=match_id)
                bowler_with_most_runs.clear()
                bowler_with_most_runs.append(bowler['bowler'])
                bowler_with_most_runs.append(bowler['total_runs_given'])
                bowler_with_most_runs.append(match.team1 + ' VS ' + match.team2 + ' at ' + match.venue)
                
                max_runs = bowler['total_runs_given']                 

        # Most number of catches by a fielder in a match for the selected season
        most_catches = 0
        fielder_with_most_catches = []
        for match_id in match_ids:
            deliveries = Deliveries.objects.filter(match_id=match_id)
            # first find out all the dismissal of caught behind..
            dismissals = deliveries.filter(dismissal_kind='caught')
            # now group by the fielder..and get the highest catch filder
            fielder = dismissals.values('fielder') \
                                .annotate(total_catches=Count('fielder')) \
                                .order_by('-total_catches').first()
            if fielder['total_catches'] > most_catches:
                # get the match..
                match = Matches.objects.get(id=match_id)
                fielder_with_most_catches.clear()
                fielder_with_most_catches.append(fielder['fielder'])
                fielder_with_most_catches.append(fielder['total_catches'])
                fielder_with_most_catches.append(match.team1 + ' VS ' + match.team2 + ' at ' + match.venue)
                
                most_catches = fielder['total_catches']   


        dataList = {
            'tosses': tosses,
            'most_awards': most_awards,
            'wins': wins,
            'venue': venue,
            'team_percenatge': team_percenatge,
            'win_by_heighest_runs': win_by_heighest_runs,
            'win_by_heighest_wkts': win_by_heighest_wkts,
            'teams_won_toss_and_match': teams_won_toss_and_match,
            'most_matches_by_locations': most_matches_by_locations,
            'top_4_teams': top_4_teams,
            'bowler_with_most_runs': bowler_with_most_runs,
            'fielder_with_most_catches': fielder_with_most_catches
        }

        context = {
            'seasons': seasons,
            'dataList': dataList,
            'template': 'home',
            'selectedSeason': season
        }
        return render(request, 'base.html', context)
    else:
        return redirect(home)




