# travelling_drunkard
pubs_f.csv contains the pub name, lattitude and longitude of pubs in the canal
google_maps_distance.py uses the google maps api to find the walking time between each pair of pubs listed in the pubs_f.csv.
These times are stored in the pub_walk_inter_distance_canals.csv file.

The pub_walk_inter_distance_canals.csv file is then used to determine the shortest path that visits each pub on foot in the travelling_drunk_process.py file.
This is a simple travelling salesman algorithm, the path is determined by moving to the nearest unvisited pub and so on. By beginning this process at 
each of the 596 pubs as a starting point, 596 unique paths are listed. The minimum of these is 58.33 km in length, marking it as the minimum path found with this algorithm.
Note that this may not be the minimum pathway between all the pubs, the travelling salesman is a notorious NP-hard problem: 
https://en.wikipedia.org/wiki/Travelling_salesman_problem

The image in the file depicts the shortest route as found with the algorithm outlined in the above python file. It was made using my data by Robert McGuinness.
