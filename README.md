# SensorSystem
## IoT project
The repository contains the project of IoT system which I did for my university's classes.

It's a system which contains multiple apps which can generate data in real time, filter and aggregate data, send data to destination the user wants, and visualise it. Each app has a configuration which the user can change with an easy interface. It is built as microservices.


### How to start system

It was run on Windows, don't know how it behaves elsewhere

```
PS C:\path\to\this\repo> python3 god.py
PS C:\path\to\this\repo> now.cmd
PS C:\path\to\this\repo> python3 server8000.py
PS C:\path\to\this\repo> python3 filter.py 
PS C:\path\to\this\repo> python3 aggregator.py 
```
The app *god* has an easy iterface to manage whole system of apps. Just go to http://localhost:8088/ in your browser and check it out.
 
When you will be on that website you will be able to see the parameters of 'checked in' sensors.
From this place you can change values of sensors' parameters, activate sensors to send data, filter data from sensors, get an average of data and draw a cute graph showing the received data.

At the start the sensors are not sending data to mqtt broker. If you want to send data you need to activate them by typing each of their names on the website and activate them. 
**Important note!** Changing parameters also activates the sensor.

Filtering data and calculating mean value are working only when data is begin sent to the default mqtt broker with default topic(s).


### How to filter data
1. On the http://localhost:8088/ type sensor's name from which you would like to filter data in the proper place and the names of columns. Example is shown below.

![](https://i.imgur.com/WJ1lJ7s.png)


### How to get an average of data
1. On the http://localhost:8088/ type sensor's name from which you would like to get an average in the proper place and time intervals. Example is shown below. After each 3 second the program takes data which he got from broker, counts the average and sends it to server. After next 3 second he counts the average from data which he got during this previous 3 second. 

![](https://i.imgur.com/rzkuK7W.png)

### How to draw a graph
1. Activate filtering or calculating mean
2. In the last field type 'filtr' or 'mean' to choose from which you would like to draw a self-updating graph in real time.
3. Go to http://localhost:8088/visual

![](https://i.imgur.com/fkUwPe3.png)

#### File contents
The webserver described in file `god.py` is a kind of manager who manages everything. From there you can see parameters of sensors, change specification of each sensor, active filter, activate calculating of average and see the graph.

The filter described in file `filter.py` after getting from mqtt broker whole line of data, takes and send to server only these data which the user have chosen on the website.

The aggregator described in file `aggregator.py` after getting from mqtt broker data which user has to specify from which sensors the data will come from, he counts the average and sends it to server. 

The file `server_8000.py` describes a flask server which gets data from *filtr* and *aggregator*. It is also the one who sends the right data for the graph.

There are 5 `.csv` files containing data, which will be used by sensors in the project: cpu_statistics, money, people, smog, temperature.

