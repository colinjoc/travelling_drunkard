"""
This finds the shortest route that allows one to visit each pub inside the canals of Dublin's fair city.  
The file "fixed_pub_walk_inter_distance_canals.csv" contains the walking time between each pair of pubs inside the canals.
The walking times were found with the googlemaps api
"""

import pandas as pd
import numpy as np

pub_times = pd.read_csv("fixed_pub_walk_inter_distance_canals.csv",sep = ",\t",names = ["Pub1","Pub2","time","distance"]) # load jobber. This is a Pandas Dataframe format.

pub_name_index = [x for x in pub_times[pub_times["Pub1"]=="The Snug Bar"]["Pub2"]] # assign an index to each pub name
pub_name_index.insert(0,"The Snug Bar") # include the snug bar

total_pubs = len(pub_name_index)

time_matrix = np.zeros(shape=(total_pubs,total_pubs)) # will store times in a matrix
dist_matrix = np.zeros(shape=(total_pubs,total_pubs)) # store distances in this matrix. Originly defined as an empty matrix

pub_data = pd.read_csv("new_pubs.csv",sep = ",",names = ["Name","X","Y"]) 

    
for x in pub_times.index: # cycle through each row in the dataframe
    index1 = pub_name_index.index(pub_times["Pub1"][x])
    index2 = pub_name_index.index(pub_times["Pub2"][x])
    
    #time_matrix[index1,index2] = pub_times["time"][x]
    if pub_times["distance"][x][-2:]!="km":
        distance = float(pub_times["distance"][x][:-1])*0.001 # sometimes the distance is in meters. converting to km
        dist_matrix[index1,index2] = distance
        dist_matrix[index2,index1] = distance
    else:
        distance = float(pub_times["distance"][x][:-2])
        dist_matrix[index1,index2] = distance
        dist_matrix[index2,index1] = distance

# method 1. nearest neighbour jumping
shortest_path = 1e20
dist_list = []
routes = []

"""
NOTES:
use a distance matrix called dist_matrix. dist_matrix[i,j] = dist_matrix[j,i] the distance between pubs i and j 

This is where the travelling salesman code starts.
1) make a list of all pubs you have to visit
2) start at a pub. delete it from list of pubs you have to visit
3) go to nearest pub. delete this pub from visit list. record the distance travelled
4) keep repeating step 3, visiting the nearest pub that has not been visited. conitnue until all pubs visited.
5) start over with a new initial pub. Repeat steps 1-4 with a new first pub each time
"""

for start_index in range(total_pubs): # start index is the index of the first pub
    check_dist_matrix = np.copy(dist_matrix)     # make copy of dist matrix. The dist matrix contains the distance between each pub and every other pub
    visit_pubs = range(total_pubs) # this list tells you what pubs you have left to visit
    current_pub = start_index 
    visited = [] # save the route
    total_distance = 0 
    while len(visit_pubs)>1:# keep repeating this until all the pubs are visited
        next_pub_dist = min(check_dist_matrix[current_pub,check_dist_matrix[current_pub].nonzero()[0]]) # find the next nearest pub
        total_distance+=next_pub_dist # add the distance
        next_index = np.where(check_dist_matrix[current_pub] == next_pub_dist)[0][0] # find the index of the next nearest pub. this checks the row of the distance matrix 
        check_dist_matrix[current_pub,:]=0 # if a pub is visited, delete its row and column from the matrix containing travel times
        check_dist_matrix[:,current_pub]=0
        visited.append(current_pub) # save the pub to the route
        visit_pubs.remove(current_pub) # remove the pub from the list of pubs you still have to visit       
        current_pub = next_index # the next pub to visit, start it all over again
        if next_index in visited: # debugging
            print "============ ERROR ================"    
    visited.append(current_pub) # save the last pub to the visited list  
    dist_list.append(total_distance) # a list of the distance this route took
    routes.append(visited) # a list of all the routes
    print total_pubs,total_distance # print em out


# this part goes through all the routes and corresponding distances above. prints em out
min_dist = min(dist_list)
min_route = routes[dist_list.index(min_dist)]
min_route_pubs = [pub_name_index[x] for x in min_route]
print min_dist, min_route


#dont mind this, saving stuff to file

pub_data = pd.read_csv("new_pubs.csv",sep = ",",names = ["Name","X","Y"]) 
min_route_gps = []
f = open("min_route_gps.csv","w")
x=0
for name in min_route_pubs:
    row_index = pub_data[pub_data["Name"]==name].index[0]
    min_route_gps.append([pub_data["X"][row_index],pub_data["Y"][row_index]])
    f.write("%s %s, %s\n" %(pub_data["X"][row_index],pub_data["Y"][row_index],name))
    x+=1
f.close()
