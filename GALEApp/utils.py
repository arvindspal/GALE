from .models import *
from django.db.models import Sum, Count

def maxWins(matches):
    try:
        wins = matches.values('winner') \
                       .annotate(wins_count=Count('winner')) \
                       .order_by('-wins_count').first()

        most_wins = wins['wins_count']
        wins = matches.values('winner') \
                       .annotate(wins_count=Count('winner')) \
                       .filter(wins_count=most_wins) \
                       .order_by('-wins_count')
    except Exception as exception:
        print(exception)
    return wins

def mostAwards(matches):
    try:
        most_awards = matches.values('player_of_match').annotate(award_count=Count('player_of_match')) \
                       .order_by('-award_count').first()
        
        most_mom = most_awards['award_count']
        most_awards = matches.values('player_of_match').annotate(award_count=Count('player_of_match')) \
                       .filter(award_count=most_mom) \
                       .order_by('-award_count')
    except Exception as exception:
        print(exception)
    return most_awards

def mostTossesWins(matches):
    try:
        tosses = matches.values('toss_winner').annotate(toss_wins_count=Count('toss_winner')) \
                       .order_by('-toss_wins_count').first()

        # there could be more than one team winning the most number of tosses..
        max_tosses_count = tosses['toss_wins_count']
        tosses = matches.values('toss_winner').annotate(toss_wins_count=Count('toss_winner')) \
                       .filter(toss_wins_count=max_tosses_count) \
                       .order_by('-toss_wins_count')

    except Exception as exception:
        print(exception)
    return tosses


def top_four_teams(matches):
    try:
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
    except Exception as exception:
        print(exception)
    return top_4_teams

def heighestWinByRuns(matches):
    try:
        winners = matches.filter(win_by_runs__gt=0) \
                        .values('winner', 'win_by_runs') \
                        .order_by('-win_by_runs').first()

        margin = winners['win_by_runs']

        winners = matches.filter(win_by_runs__gt=0) \
                        .values('winner', 'win_by_runs') \
                        .filter(win_by_runs=margin) \
                        .order_by('-win_by_runs')
    except Exception as exception:
        print(exception)
    return winners


def heighestWinByWkts(matches):
    try:
        winners = matches.filter(win_by_wickets__gt=0) \
                        .values('winner', 'win_by_wickets') \
                        .order_by('-win_by_wickets').first()

        margin = winners['win_by_wickets']

        winners = matches.filter(win_by_wickets__gt=0) \
                        .values('winner', 'win_by_wickets') \
                        .filter(win_by_wickets=margin) \
                        .order_by('-win_by_wickets')
    except Exception as exception:
        print(exception)
    return winners

def locationHostedMostMatches(matches):
    try:
        locations = matches.values('venue') \
                       .annotate(matches_count=Count('venue')) \
                       .order_by('-matches_count').first()

        counts = locations['matches_count']

        locations = matches.values('venue') \
                       .annotate(matches_count=Count('venue')) \
                       .filter(matches_count=counts) \
                       .order_by('-matches_count')
    except Exception as exception:
        print(exception)
    return locations


def mostRunsGiven(matches):
    bowlers = {}
    try:
        max_runs = 0
        match_ids = matches.values_list('id', flat=True).distinct()
        for match_id in match_ids:
            deliveries = Deliveries.objects.filter(match_id=match_id)
            # now group this by bowler..
            bowler = deliveries.values('bowler') \
                                .annotate(runs_given=Sum('total_runs')) \
                                .order_by('-runs_given').first()

            if bowler['runs_given'] > max_runs:
                # get the match..
                match = Matches.objects.get(id=match_id)
                bowlers.clear()
                bowlers['bowler'] = bowler['bowler']
                bowlers['runs_given'] = bowler['runs_given']
                bowlers['venue'] = match.team1 + ' VS ' + match.team2 + ' at ' + match.venue
                max_runs = bowler['runs_given']  
    except Exception as exception:
        print(exception)
    return bowlers


def mostCatches(matches):
    fielders = {}
    try:
        match_ids = matches.values_list('id', flat=True).distinct()
        most_catches = 0
        for match_id in match_ids:
            deliveries = Deliveries.objects.filter(match_id=match_id)
            # first find out all the dismissal of caught behind..
            dismissals = deliveries.filter(dismissal_kind='caught')
            # now group by the fielder..and get the highest catch filder
            fielder = dismissals.values('fielder') \
                                .annotate(catches=Count('fielder')) \
                                .order_by('-catches').first()
            if fielder['catches'] > most_catches:
                # get the match..
                match = Matches.objects.get(id=match_id)
                fielders.clear()
                fielders['fielder'] = fielder['fielder']
                fielders['catches'] = fielder['catches']
                fielders['venue'] = match.team1 + ' VS ' + match.team2 + ' at ' + match.venue
                most_catches = fielder['catches']  
    except Exception as exception:
        print(exception)
    return fielders


def teamsBattedFirstWhenWonToss(matches):
    try:
        total_matches = matches.count()
        teams_batted_first = matches.filter(toss_decision='bat').count()

        if total_matches > 0:
            percenatge = (teams_batted_first/total_matches) * 100
        else:
            percenatge = 0    
    except Exception as exception:
        print(exception)
    return percenatge