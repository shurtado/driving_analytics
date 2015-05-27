import re
import sys
import glob
import getopt
import datetime
import fnmatch
import os

def format(data):

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

def parse(filename):

    data = []

    indicator = re.compile('^[0-9]{13}(?=:)')

    with open(filename) as f:

        for line in f.readlines():

            if re.match(indicator, line):

                line = line.strip().split(':')

                datum = format(line)

                data.append(datum)

    return data


if __name__ == "__main__":

    """
    Read command line args
    """

    path = '.'

    pipe = 'example'

    try:
        opts, args = getopt.getopt(sys.argv[1:], '', ['path=', 'pipe='])
    except getopt.GetoptError:
        print 'parser.py --path <path> --pipe <pipe>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '--path':
            path = arg
        elif opt == '--pipe':
            pipe = arg


    """
    Parse files
    """

    print 'Looking:', path

    files = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, 'carData.txt'):
            files.append(os.path.join(root, filename))

    data = []

    for f in files:
        print 'Reading:', f
        data.append(parse(f))


    """
    Pipe output
    """

    print 'Piping to:', pipe

    module = __import__(pipe)

    module.run(data)
    