
def run(data):

    max = 0

    for experiment in data:

        for t in experiment:
            if t['speed'] > max:
                max = t['speed']

        print 'The max speed is', max
