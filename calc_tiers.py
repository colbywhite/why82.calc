import argparse
import simplejson as json
import why82.tiers as tiers


def calc_tiers(stats):
    return tiers.calc(stats)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate team tiers based on stats')
    parser.add_argument('file', metavar='FILE', type=argparse.FileType('r'), help='File to read stats from')

    args = parser.parse_args()
    stats_input = json.loads(args.file.read())
    tiers = calc_tiers(stats_input)
    print('pace tier 1:')
    print(', '.join({team for (team, info) in tiers.iteritems() if info['pace']['tier'] == 1}))
    print('win_loss tier 1:')
    print(', '.join({team for (team, info) in tiers.iteritems() if info['win_loss']['tier'] == 1}))
