import math
import json
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import copy


class Coordinates:
    def __init__(self, lng, lat):
        self.lng = lng
        self.lat = lat


class ParkedCar:
    def __init__(self, num, coords):
        self.num = num
        self.coords = coords


class Canopies:
    def __init__(self, num, coords):
        self.num = num
        self.coords = coords

fig = plt.figure()

directory = 'C:\\Users\\User\Desktop\part_nodes'
files = os.listdir(directory)
json_files = filter(lambda x: x.endswith('.json'), files)
S = list(json_files)
coord_list = []
for i in range(len(S)):
    coord_list.append([])

for i in range(len(S)):
    with open('C:\\Users\\User\Desktop\part_nodes\{}'.format(S[i]), 'r') as inf:
        for j in inf:
            json_string = inf.readline()
            try:
                coord_list[i].append(json.loads(json_string))
            except ValueError:
                print('Can not decode this string')

for i in range(len(coord_list)):
    coord_list[i] = list(filter(lambda x: 'sat_cnt' in x.keys(), coord_list[i]))
    coord_list[i] = list(filter(lambda x: 'speed' not in x.keys(), coord_list[i]))


def distance(x1, x2, y1, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

epsilon = 0.00183               # погрешность в определении местоположения в 100 метров
parked_cars = []

for i in range(len(coord_list)):
    parking_time = 0
    for j in range(len(coord_list[i]) - 1):
        if distance(coord_list[i][j]['lng'], coord_list[i][j + 1]['lng'], coord_list[i][j]['lat'],
                    coord_list[i][j + 1]['lat']) <= epsilon:
            parking_time += coord_list[i][j + 1]['ts'] - coord_list[i][j]['ts']
        else:
            if parking_time > 3600:
                car = ParkedCar(i, Coordinates(coord_list[i][j]['lng'], coord_list[i][j]['lat']))
                parked_cars += [car]
            parking_time = 0

cars_to_draw = copy.deepcopy(parked_cars)

canopies_list = []
T1 = 0.0041                 # 350 метров
T2 = 0.0012                 # 100 метров
canopy_num = 0
while len(parked_cars) > 1:
    canopies_list.append(parked_cars[0])
    i = 0
    while i < len(parked_cars) - 1:
        d = distance(parked_cars[0].coords.lng, parked_cars[i + 1].coords.lng, parked_cars[0].coords.lat,
                     parked_cars[i + 1].coords.lat)
        if d <= T1:
            canopies_list.append(parked_cars[i + 1])
            if d <= T2:
                parked_cars.remove(parked_cars[i + 1])
        i += 1
    canopy_num += 1
    parked_cars.remove(parked_cars[0])

xs = []
ys = []
for i in range(len(cars_to_draw)):
    xs += [cars_to_draw[i].coords.lng]
    ys += [cars_to_draw[i].coords.lat]

print("Started")
circles_to_draw = []
i = 0
while i < len(canopies_list) - 1:
    circles_to_draw.append(canopies_list[i])
    j = canopies_list[i].num
    while j == canopies_list[i].num and i < len(canopies_list) - 1:
        i += 1
        print(str(i))
print("Ended")

circle = []
circle1 = []
for i in range(len(circles_to_draw)):
    circle.append(plt.Circle((circles_to_draw[i].coords.lng, circles_to_draw[i].coords.lat), radius=T2, fill=False))
    circle1.append(plt.Circle((circles_to_draw[i].coords.lng, circles_to_draw[i].coords.lat), radius=T1, fill=False))

for i in range(len(circle)):
    plt.gca().add_artist(circle[i])
    plt.gca().add_artist(circle1[i])

plt.scatter(xs, ys, s=1)
plt.grid(True)
plt.show()
