def build_file_name(save_date, season, suffix=None):
    # correct the date for when it falls outside of the season boundaries
    correct_date = save_date
    if save_date <= season['start']:
        correct_date = season['start']
    elif season['end'] < save_date:
        correct_date = season['end']
    if suffix:
        return '%s/%s-%s.json' % (season['name'], correct_date.strftime('%Y-%m-%d'), suffix)
    else:
        return '%s/%s.json' % (season['name'], correct_date.strftime('%Y-%m-%d'))
