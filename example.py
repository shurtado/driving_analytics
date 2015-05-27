
def run(data):

    print "We have parsed", len(data), "experiments."

    view = raw_input('View parsed data (y/n)? ')

    if(view.lower() == 'y'):
        print data
