import os
import simplejson as json
from decimal import Decimal

OVERALL_TIER_ONE_MAX = Decimal(1.666)
OVERALL_TIER_TWO_MAX = Decimal(2.333)

def calc_overall(tiers, result={}):
    weights, total_weight = load_weight_config()
    for name, info in tiers.iteritems():
        weighted_sum = Decimal(0)
        for metric, values in info.iteritems():
            weight = weights[metric]
            weighted_val = values['tier'] * weight
            weighted_sum += Decimal(weighted_val)
        weighted_avg = weighted_sum / total_weight
        team = result.get(name, {})
        team['overall'] = {'avg': weighted_avg, 'tier': calc_overall_tier(weighted_avg)}
        result[name] = team
    return result


def calc_overall_tier(tier_avg):
    if tier_avg <= OVERALL_TIER_ONE_MAX:
        return 1
    elif tier_avg > OVERALL_TIER_ONE_MAX and tier_avg <= OVERALL_TIER_TWO_MAX:
        return 2
    else:
        return 3


def load_weight_config():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    weights_file = "%s/weights.json" % dir_path
    with open(weights_file, 'r') as f:
        weights = json.loads(f.read())
    total_weight = reduce(lambda x, y: x +y, weights.values())
    return (weights, Decimal(total_weight))
