import re
import sys
import glob
import getopt
import datetime
import fnmatch
import os

def formatData(data):

    return {
        'time': datetime.datetime.fromtimestamp(int(data[0]) / 1000),
        'position': {'x': float(data[1]), 'y': float(data[2]), 'z': float(data[3])},
        'rotation': {'x': data[4], 'y': data[5], 'z': data[6], 'w': data[7]},
        'speed': float(data[8]),
        'steering_wheel_position': float(data[9]),
        'gas_pedal_position': float(data[10]),
        'brake_pedal_position': float(data[11]),
        'engine_running': True if data[12] == 'true' else False
    }

def parseData(filename):

    data = []

    indicator = re.compile('^[0-9]{13}(?=:)')

    with open(filename) as f:

        for line in f.readlines():

            if re.match(indicator, line):

                line = line.strip().split(':')

                datum = formatData(line)

                data.append(datum)

    return data


def formatMeta(meta):

    meta['start_time'] = datetime.datetime.strptime(meta['start_time'], '%Y-%m-%d %H:%M:%S.%f')

    return meta

def parseMeta(filename):

    meta = {}

    with open(filename) as f:

        for line in f.readlines():

            try:
                key, val = line.strip().split(': ')

                key = key.lower().replace(' ', '_')

                meta[key] = val

            except:
                pass

    return formatMeta(meta)


if __name__ == "__main__":

    """
    Read command line args
    """

    path = '.'

    pipe = 'example'

    filter = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], '', ['path=', 'pipe=', 'filter='])
    except getopt.GetoptError:
        print 'parser.py --path <path> --pipe <pipe>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '--path':
            path = arg
        elif opt == '--pipe':
            pipe = arg
        elif opt == '--filter':
            filter = arg


    """
    Parse files
    """

    print 'Looking:', path

    files = []

    for root, dirnames, filenames in os.walk(path):

        info = []

        for f in ['drivingTaskLog.txt', 'carData.txt']:
            for filename in fnmatch.filter(filenames, f):
                info.append(os.path.join(root, filename))

        if len(info) == 2:
            files.append(info)

    data = []

    for m, d in files:
        print 'Reading:\n  ', m, '\n  ', d
        data.append({'meta': parseMeta(m), 'data': parseData(d)})


    """
    Filter data
    """

    if filter:

        print 'Filtering:', filter

        filtered = []
        
        try:
            key, val = filter.split('=')

            for datum in data:

                if datum['meta'][key] == val:
                    filtered.append(datum)

        except:
            pass

        data = filtered


    """
    Pipe output
    """

    print 'Piping to:', pipe, '\n'

    module = __import__(pipe)

    module.run(data)
    