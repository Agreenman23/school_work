# Databricks notebook source
#ALEX GREENMAN

import os
from itertools import combinations
import math

sc = spark.sparkContext

#Create directories to store CSV files containing points data
dbutils.fs.mkdirs("FileStore/tables/AssignmentOne")
dbutils.fs.mkdirs("FileStore/tables/AssignmentOne/AssignmentOneData")

fileDirectory = '/dbfs/FileStore/tables/'
direc = '/FileStore/tables/'

for filename in os.listdir(fileDirectory):
  if "geo" in filename:
    dbutils.fs.mv(direc+filename, "FileStore/tables/AssignmentOne/AssignmentOneData")

# COMMAND ----------

geoData = sc.textFile('dbfs:///FileStore/tables/AssignmentOne/AssignmentOneData')

#Define functions to format raw points data and then place points into grid cells

def Convert(intake): 
  out = tuple(intake.split(",")) 
  out = (out[0], float(out[1]), float(out[2]))
  return out

def place_in_cells(alpha_num_name, x_val, y_val, cell_size):
  #Calculate integer x,y coordinate values for floating point coordinates
  xCell = int(math.floor(x_val/cell_size))
  yCell = int(math.floor(y_val/cell_size))
  #Map to the cells three below and one to the right of the target cell
  neighbor_cells = [(xCell, yCell), 
                    (xCell + cell_size, yCell),
                    (xCell, yCell - cell_size), 
                    (xCell-cell_size, yCell-cell_size), 
                    (xCell + cell_size, yCell-cell_size)]
  list_of_neighbor_cells = []
  for cell in neighbor_cells:
    list_of_neighbor_cells.append((cell, (alpha_num_name, x_val, y_val)))
  return list_of_neighbor_cells

points = geoData.map(lambda x: Convert(x))

points_to_cells = points.map(lambda point: place_in_cells(point[0], point[1], point[2], 1))

points_to_cells_flat = points_to_cells.flatMap(lambda x: [i for i in x])

# Use combineByKey to create pair RDDs that group all the point objects for a cell
points_grouped_by_cell = points_to_cells_flat.combineByKey(
        #Create a Combiner - function to be used as the very first aggregation step for each key. Turn value into a list
        lambda value: [value],
        #Merge a Value - takes a value and merges/combines it into the previously collected values.
        lambda new_values, value: new_values + [value],
        #Combine the merged values together - takes the new values produced at the partition level and combines them into a singular value for each key.
        lambda new_values_1, new_values_2: new_values_1 + new_values_2)

#Persist mapping of grid cells as it will be used multiple times
points_grouped_by_cell_sorted = points_grouped_by_cell.sortByKey().persist()


# COMMAND ----------

#Create function to calculate distance between points
def distance_between_points(x_point_one, x_point_two, y_point_one, y_point_two):
  distance = math.sqrt(((x_point_two-x_point_one)**2)+((y_point_two-y_point_one)**2))
  return distance

#Create function to find pairs where at least one point is inside the cell being processed and the calculate the distance between
def find_distances_add_on(x, *distance_to_check):
  point_combo_and_distances = []
  combo_list = []
  count_and_points = []
  #Find all combinations of points that have been mapped to a certain grid cell
  combos = combinations(x[1], 2)
  for elements in combos:
    combo_list.append(elements)
  #Make sure that the combination of pairs are in the same grid cell before processing their distance
  for each_combo in combo_list:
    raw_coords_one = (each_combo[0][1],each_combo[0][2])
    raw_coords_two = (each_combo[1][1],each_combo[1][2])
    coordinates_one = ((int(math.floor(each_combo[0][1]))),(int(math.floor(each_combo[0][2]))))
    coordinates_two = ((int(math.floor(each_combo[1][1]))),(int(math.floor(each_combo[1][2]))))
    #If points are in the same grid cell, calculate their distance
    if (coordinates_one == x[0]) or (coordinates_two == x[0]):
      distance = distance_between_points(raw_coords_one[0],raw_coords_two[0],raw_coords_one[1], raw_coords_two[1])
      #For points in the same grid cell, check their distance apart again the list of distances
      for dists in distances_to_check:
        if distance<=dists:
          point_combo_and_distances.append((dists,each_combo[0][0],each_combo[1][0]))
  return point_combo_and_distances

distances_to_check = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]

#flatMap with distance function
distances = points_grouped_by_cell_sorted.flatMap(lambda x: find_distances_add_on(x, *distances_to_check)).persist()

#Create pair RDD where distances are the keys, and the values are coorinate pairs that are within that distance
pairs = distances.map(lambda x: (x[0], x[1:])) 

#groupBykey on distances and convert values to a list so that len() can be used to count number of pair tuples
#collect rdd so that it is a list that can be iterated over to produce desired print outs
to_list = pairs.groupByKey().map(lambda x : (x[0], list(x[1]))).collect()

for dti in distances_to_check:
  print('Dist:', dti)
  for keys in to_list:
    if keys[0] == dti:
      print(len(keys[1]),keys[1])
      print()


# COMMAND ----------


