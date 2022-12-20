
def stats(user):
    user_stats = {}
    user_stats['wins'] = user.wins
    user_stats['wins_as_hunter'] = user.wins_as_hunter
    user_stats['wins_as_hider'] = user.wins - user.wins_as_hunter
    user_stats['games_played'] = user.games_played
    if (user_stats['games_played'] == 0):
        user_stats['win_rate'] = 0
    else:
        user_stats['win_rate'] = user.wins / user.games_played * 100
    if (user_stats['games_played'] == 0):
        user_stats['best_role'] = "Newbie"
    elif (user_stats['wins_as_hunter'] > user_stats['wins_as_hider']):
        if ((user_stats['wins_as_hunter'] / user_stats['wins'] ) > 0.6):
            user_stats['best_role'] = "Pro-Hunter"
        else:
            user_stats['best_role'] = "Hunter"
    elif (user_stats['wins_as_hunter'] < user_stats['wins_as_hider']):
        if ((user_stats['wins_as_hider'] / user_stats['wins'] ) > 0.6):
            user_stats['best_role'] = "Pro-Hinder"
        else:
            user_stats['best_role'] = "Hinder"
    elif (user_stats['wins_as_hunter'] == user_stats['wins_as_hider']):
        user_stats['best_role'] = "Balanced Player"
    return user_stats
