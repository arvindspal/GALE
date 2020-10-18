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
from .utils import *
from .serializers import *


# Create your views here.

def home(request):
    seasons = Matches.objects.values_list('season', flat=True).order_by('-season').distinct()
    context = {
        'seasons': seasons,
        'template': 'home'
    }
    return render(request, 'base.html', context)


@api_view(['GET'])
def getSeasons(request): 
    try:
        seasons = Matches.objects.values_list('season', flat=True).order_by('-season').distinct()
    except Matches.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(seasons)


@api_view(['GET'])
def getStatistics(request, season):
    
    dataList = {}
    default_items = []
    labels = []
    try:
        season = int(season)
        matches = Matches.objects.filter(season=season)
        # top 4 teams in terms of wins..
        teams = matches.values('winner') \
                    .annotate(wins_count=Count('winner')) \
                    .order_by('-wins_count')[:4]

        for team in teams:
            labels.append(team['winner'])
            default_items.append(team['wins_count'])

        top_teams = {
            'labels': labels,
            'defaults': default_items
        }
        dataList['top_teams'] = top_teams

        # most number of tosses wins..
        tosses = mostTossesWins(matches)
        dataList['tosses'] = tosses
        
        # most number of player of the match awards..
        awards = mostAwards(matches)
        dataList['awards'] = awards

        # max wins by team.
        wins = maxWins(matches)
        dataList['wins'] = wins

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

        dataList['venue'] = venue
        # Which % of teams decided to bat when they won the toss
        # get total number of matches for the season..
        percenatge = teamsBattedFirstWhenWonToss(matches)
        dataList['percenatge'] = percenatge

        # Which team won by the highest margin of runs  for the season
        runs_margin = heighestWinByRuns(matches)
        dataList['runs_margin'] = runs_margin
        
        # Which team won by the highest number of wickets for the season
        wkts_margin = heighestWinByWkts(matches)
        dataList['wkts_margin'] = wkts_margin
        
        # How many times has a team won the toss and the match
        teams_won_toss_and_match = matches.filter(toss_winner=F('winner')).count()
        dataList['teams_won_toss_and_match'] = teams_won_toss_and_match

        #Which location hosted most number of matches and win % and loss % for the season
        most_matches_by_locations = locationHostedMostMatches(matches)
        dataList['most_matches_by_locations'] = most_matches_by_locations
        
        # Which Batsman (or bowler?) gave away the most number of runs in a match for the selected season
        # get match IDs for the season..
        most_runs_given = mostRunsGiven(matches)
        dataList['most_runs_given'] = most_runs_given

        # Most number of catches by a fielder in a match for the selected season
        most_catches = mostCatches(matches)
        dataList['most_catches'] = most_catches

    except Matches.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(dataList)

