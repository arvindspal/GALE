from .models import *
from django.db.models import Sum, Count

def max_wins_by_team(matches):
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

def most_player_awards(matches):
    try:
        most_awards = matches.values('player_of_match').annotate(player_of_match_wins_count=Count('player_of_match')) \
                       .order_by('-player_of_match_wins_count').first()
        
        most_mom = most_awards['player_of_match_wins_count']
        most_awards = matches.values('player_of_match').annotate(player_of_match_wins_count=Count('player_of_match')) \
                       .filter(player_of_match_wins_count=most_mom) \
                       .order_by('-player_of_match_wins_count')
    except Exception as exception:
        print(exception)
    return most_awards

def most_tosses_wins(matches):
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

def heighest_win_by_runs(matches):
    try:
        win_by_heighest_runs = matches.filter(win_by_runs__gt=0) \
                        .values('winner', 'win_by_runs') \
                        .order_by('-win_by_runs').first()

        heighest_margin_by_run = win_by_heighest_runs['win_by_runs']

        win_by_heighest_runs = matches.filter(win_by_runs__gt=0) \
                        .values('winner', 'win_by_runs') \
                        .filter(win_by_runs=heighest_margin_by_run) \
                        .order_by('-win_by_runs')
    except Exception as exception:
        print(exception)
    return win_by_heighest_runs


def heighest_win_by_wkts(matches):
    try:
        win_by_heighest_wkts = matches.filter(win_by_wickets__gt=0) \
                        .values('winner', 'win_by_wickets') \
                        .order_by('-win_by_wickets').first()

        highest_wkt_margin = win_by_heighest_wkts['win_by_wickets']

        win_by_heighest_wkts = matches.filter(win_by_wickets__gt=0) \
                        .values('winner', 'win_by_wickets') \
                        .filter(win_by_wickets=highest_wkt_margin) \
                        .order_by('-win_by_wickets')
    except Exception as exception:
        print(exception)
    return win_by_heighest_wkts

def location_hosted_most_matches(matches):
    try:
        most_matches_by_locations = matches.values('venue') \
                       .annotate(matches_count=Count('venue')) \
                       .order_by('-matches_count').first()

        most_match_count = most_matches_by_locations['matches_count']

        most_matches_by_locations = matches.values('venue') \
                       .annotate(matches_count=Count('venue')) \
                       .filter(matches_count=most_match_count) \
                       .order_by('-matches_count')
    except Exception as exception:
        print(exception)
    return most_matches_by_locations


def most_number_of_runs(matches):
    bowler_with_most_runs = []
    try:
        max_runs = 0
        match_ids = matches.values_list('id', flat=True).distinct()
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
    except Exception as exception:
        print(exception)
    return bowler_with_most_runs


def most_number_of_catches(matches):
    fielder_with_most_catches = []
    try:
        match_ids = matches.values_list('id', flat=True).distinct()
        most_catches = 0
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
    except Exception as exception:
        print(exception)
    return fielder_with_most_catches