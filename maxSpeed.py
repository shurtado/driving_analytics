
def run(data):

    for exp in data:

        maxSpeed = 0

        for t in exp['data']:
            if t['speed'] > maxSpeed:
                maxSpeed = t['speed']

        print exp['meta']['driver'], 'max speed was', maxSpeed, 'on track', exp['meta']['driving_task']
