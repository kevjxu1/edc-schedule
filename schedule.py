#!/usr/bin/python3
import os

def get_human_format_time_sort_key(human_time):
    """
    e.g. 8:15PM
    """
    hh, mm = human_time[:-2].split(':')
    if human_time.upper().endswith('AM'):
        # add 24 hours because it is next day
        t24_hh = (int(hh) % 12) + 24
    else:  # PM
        t24_hh = (int(hh) % 12) + 12

    t24 = '{0}:{1}'.format(t24_hh, mm)
    return t24

if __name__ == '__main__':
    raw_dir = os.path.join(os.curdir, 'raw')
    dirs = os.listdir(raw_dir)
    for day in dirs:
        rows = []
        full_dir = os.path.join(raw_dir, day)
        files = os.listdir(full_dir)
        for fname in files:
            stage, _ext = os.path.splitext(fname)
            full_file = os.path.join(full_dir, fname)
            with open(full_file, 'r') as f:
                lines = [ l.rstrip().lstrip() for l in f.readlines() ]
                for l in lines:
                    tokens = l.split()
                    start_time, end_time, artist = tokens[0], tokens[2], str.join(' ', tokens[3:])
                    row = [ artist, start_time, end_time, stage ]
                    rows.append(row)

        rows.sort(key=lambda r: (get_human_format_time_sort_key(r[1]), get_human_format_time_sort_key(r[2])))
        out_file = '{0}.csv'.format(day)
        with open(out_file, 'w') as f:
            for r in rows:
                f.write(str.join(',', r) + '\n')
