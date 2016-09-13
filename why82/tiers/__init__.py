from decimal import Decimal

PACE_TIER_ONE_CUTOFF = Decimal('98.5')
PACE_TIER_TWO_CUTOFF = Decimal('97.0')


def calc_pace(team_stats, result={}):
    for name, stats in team_stats.iteritems():
        pace_stat = stats['pace']
        if pace_stat < PACE_TIER_TWO_CUTOFF:
            tier = 3
        elif PACE_TIER_TWO_CUTOFF <= pace_stat < PACE_TIER_ONE_CUTOFF:
            tier = 2
        else:
            tier = 1
        result[name]['pace'] = {'tier': tier, 'pace': pace_stat}
    return result


WIN_LOSS_TIER_ONE_CUTOFF = Decimal('.660')
WIN_LOSS_TIER_TWO_CUTOFF = Decimal('.550')


def calc_win_loss(team_stats, result={}):
    for name, stats in team_stats.iteritems():
        win_loss_pct = stats['win_loss_pct']
        wins = stats['wins']
        losses = stats['losses']
        if win_loss_pct < WIN_LOSS_TIER_TWO_CUTOFF:
            tier = 3
        elif WIN_LOSS_TIER_TWO_CUTOFF <= win_loss_pct < WIN_LOSS_TIER_ONE_CUTOFF:
            tier = 2
        else:
            tier = 1
        team = result.get(name, {})
        team['win_loss'] = {'tier': tier, 'win_loss_pct': win_loss_pct, 'wins': wins, 'losses': losses}
        result[name] = team
    return result


def calc(team_stats):
    return calc_pace(team_stats, calc_win_loss(team_stats))
