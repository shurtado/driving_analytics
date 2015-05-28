# Driving Analytics

### How to run

```shell
python parser.py [--path] [--pipe] [--filter]
```

### Options

#### --path

Path to the anaylzerData folder.


#### --pipe

After the data has been parsed, the `pipe` module is loaded, and the run function is 
executed with the parsed data.

For example:
```shell
python parser.py --path ./analyzerData --pipe maxSpeed
```

Will execute:
```python
maxSpeed.run(data)

# data = [
#   [
#     {
#       'meta': {},
#       'data': []
#    }
#   ]
# ]
```

Where `'meta'` contains all key:value pairs in drivingTaskLog.txt and `'data'` contains a
list of all data points in carData.txt.


#### --filter

A key:value pair to filter the data.

Fitler for a specific driver:
```shell
python parser.py --filter driver="driver 1"
```

Filter by a track:
```shell
python parser.py --filter driving_task="highway_germany.xml"
```
