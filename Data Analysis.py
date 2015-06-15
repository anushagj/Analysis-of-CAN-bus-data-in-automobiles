#Mini-Project1
#This file contains 8 functions pertaining to the 8 questions in the project.
#It is sufficient to enter the name of the file without extension. This script adds .json extension while reading the file.

import json
import os
path = os.path.dirname(os.path.realpath(__file__))
path = path + '\\pygmaps-0.1.1'
import sys
sys.path.append(path)
import pygmaps
path = os.path.dirname(os.path.realpath(__file__))
path = path + '\\six-1.9.0'
sys.path.append(path)
from pprint import pprint
import numpy
path = os.path.dirname(os.path.realpath(__file__))
path = path + '\\python-dateutil-2.4.1'
sys.path.append(path)
import pylab

#function 1 definition
#This function reads the JSON file and returns a list of python dictionaries.
def func1(data_file):
    #Storing file name in a string
    data_file = data_file + ".json"
    #Declaring an empty list to read data file as a Python list of Python dictionary items
    signal_data = []
    with open(data_file, "r") as f:
        for line in f:
            signal_data.append(json.loads(line))
    print('Data loaded')
    return signal_data


#function 2 definition
#This function accepts the processed data as input and prints the first 10 list items
def func2(signal_data):
    #Using pprint to print the first 10 list items
    print('Printing first 10 elements of the list')
    pprint(signal_data[:10])
    

#function 3 definition
#This function prints all the different signals in the list.
#It then prints the number of occurences and the range for the signal that the user inputs.
def func3(signal_data):
    #Declaring an empty dictionary
    signals = {}
    #Initializing all the values to empty list
    for line in signal_data:
        signals[line['name']] = []
    #Appending the values to the corresponding key in the dictionary
    for line in signal_data:
        signals[line['name']].append(line['value'])
    print("The different signals are")
    #Printing all the keys-->signals
    for signal in signals.keys():
        print(signal)
    input_signal = input("Enter the name of the signal for which you want the details : ")
    #Storing the list of values corresponding to the entered signal
    values = signals[input_signal]
    print("The number of occurances of the signal {0} is {1}".format(input_signal, len(values)))
    print("The Range for this signal is {0} and {1}".format(min(values), max(values)))
    
          
    
#function 4 definition
#This function finds the vehicle trip duration and trip distance.
#It calculates the average speed and time to find the distance.
def func4(signal_data):
    #Declaring an empty list for timestamp values
    time = []
    for line in signal_data:
        time.append(float(line['timestamp']))
    #Finding the time duration
    duration = (max(time)- min(time))
    print("The vehicle trip duration is {0:.2f} seconds".format(duration))
    #Declaring an empty list for vehicle_speed values
    speed = []
    for line in signal_data:
        if 'vehicle_speed' in line.values():
            speed.append(float(line['value']))
    #Finding the average speed of the vehicle for the trip duration
    average_speed = float(sum(speed) / len(speed))
    #Finding the distance travelled during the trip
    distance = (average_speed*duration)/3600
    print("The vehicle trip distance is {0:.2f} miles".format(distance))


#function 5 definition
#This function plots the different signals with time.
def func5(signal_data):
    signals = {}
    #Initializing all the values to empty list
    for line in signal_data:
        signals[line['name']] = []
    #Appending the values to the corresponding key in the dictionary
    for line in signal_data:
        signals[line['name']].append([line['value'],line['timestamp']])
    for signal in signals.keys():
        print('Plotting {} Vs time'.format(signal))
        x = []
        y = []
        if (signal != 'brake_pedal_status') and (signal != 'transmission_gear_position'):
            for line in signals[signal]:
                y.append(line[0])
                x.append(line[1])
            pylab.plot(x,y)
            pylab.xlabel('Time')
            pylab.ylabel(signal)
            title = signal + ' Vs ' + 'time'
            pylab.title(title)
            pylab.show()
            print('Close the plot to see the next plot')
        if  (signal == 'transmission_gear_position'):
            for line in signals[signal]:
                x.append(line[1])
                if line[0] == 'first':
                    y.append(1)
                if line[0] == 'second':
                    y.append(2)
                if line[0] == 'third':
                    y.append(3)
                if line[0] == 'fourth':
                    y.append(4)
                if line[0] == 'neutral':
                    y.append(5)
            pylab.plot(x,y)
            pylab.xlabel('Time')
            pylab.ylabel(signal)
            title = signal + ' Vs ' + 'time'
            pylab.title(title)
            pylab.show()
            print('Close the plot to see the next plot')
    

#function 6 definition
#This function finds the maximum and average speed of the vehicle.
def func6(signal_data):
    #Declaring an empty list for vehicle_speed values
    speed = []
    for line in signal_data:
        if 'vehicle_speed' in line.values():
            speed.append(float(line['value']))
    #Finding the maximum speed of the vehicle for the trip duration
    max_speed = max(speed)
    #Finding the average speed of the vehicle for the trip duration
    average_speed = float(sum(speed) / len(speed))
    print("The maximum speed of the vehicle is {0:.2f} mph".format(max_speed))
    print("The average speed of the vehicle is {0:.2f} mph".format(average_speed))


#function 7 definition
#This function draws the vehicle's path on a google map.
def func7(signal_data):
    #Declaring an empty list to hold the list of coordinates
    coordinates = []
    #Declaring a smaller list to hold the current coordinates
    position = []
    count = 0
    for line in signal_data:
        if 'latitude' in line.values() and count is 0:
            position.append(float(line['value']))
            count = count + 1
            continue
        if 'latitude' in line.values() and count is 1:
            position.insert(0,float(line['value']))
            coordinates.append(tuple(position))
            #Reinitialize position to empty list when both coordinates are found
            position = []
            count = 0
            continue
        if 'longitude' in line.values() and count is 0:    
            position.append(float(line['value']))
            count = count + 1
            continue
        if 'longitude' in line.values() and count is 1:    
            position.append(float(line['value']))
            coordinates.append(tuple(position))
            #Reinitialize position to empty list when both coordinates are found
            position = []
            count = 0
            continue
    print('Map file created')
    mymap = pygmaps.maps(coordinates[0][0], coordinates[0][1],15)
    mymap.addpath(coordinates, "#FF0000")
    mymap.draw('./mymap.html')


#function 8 definition
#This function plots the points where the vehicle stopped on a google map.
def func8(signal_data):
    #Creating a dictionary with keys and values as times when vehicle speed was zero
    #We want for 1 second resolution and we want distinct time values
    timestamps = {}
    for line in signal_data:
        if ('vehicle_speed' in line.values()) and (float(line['value']) == 0):
            time = float(line['timestamp'])
            timestamps[round(time, 0)] = 1
    #Declaring an empty list to hold the list of coordinates
    coordinates = {}
    #Declaring a smaller list to hold the current coordinates
    position = []
    count = 0
    for line in signal_data:
        if 'latitude' in line.values() and count is 0:
            position.append(float(line['value']))
            count = count + 1
            continue
        if 'latitude' in line.values() and count is 1:
            position.insert(0,float(line['value']))
            time = float(line['timestamp'])
            coordinates[round(time, 0)] = (tuple(position))
            #Reinitialize position to empty list when both coordinates are found
            position = []
            count = 0
            continue
        if 'longitude' in line.values() and count is 0:    
            position.append(float(line['value']))
            count = count + 1
            continue
        if 'longitude' in line.values() and count is 1:    
            position.append(float(line['value']))
            time = float(line['timestamp'])
            coordinates[round(time, 0)] = (tuple(position))
            #Reinitialize position to empty list when both coordinates are found
            position = []
            count = 0
            continue
    #Creating a list of points where we have latitude and longitude values for times when vehicle speed was zero
    points = []
    for time in timestamps.keys():
        for line in coordinates.keys():
            if (time == line):
                points.append(coordinates[line])
    #Plotting those points on a google map
    mymap = pygmaps.maps(points[0][0], points[0][1],20)
    for point in points:
        mymap.addpoint(point[0], point[1], "#FF0000")
    print('Created a plot--> check mystop.html file')
    mymap.draw('./mystop.html')
    
