import googlemaps as gm # pip install googlemaps, contains some of the 
import numpy as np
import pandas as pd
import time
import codecs

api_key = open("google_maps_api.key","r").read()
gmaps = gm.Client(key = api_key)

pub_data = pd.read_csv("pubs_f.csv",sep = ",",names = ["Name","X","Y"])

for index1 in range(0,len(pub_data)):
	for index2 in range(index1+1,len(pub_data)):
		if index1!=index2:
			out = codecs.open("pub_walk_inter_distance.csv","a",encoding='utf-8')
			name1 = pub_data["Name"][index1]
			name2 = pub_data["Name"][index2]

			Lat1 = pub_data["X"][index1]
			Lat2 = pub_data["X"][index2]

			Long1 = pub_data["Y"][index1]
			Long2 = pub_data["Y"][index2]


			dist =gmaps.distance_matrix([[Lat1,Long1]],[[Lat2,Long2]], mode = "walking")
			t = dist['rows'][0]['elements'][0]['duration']['text']
			d = dist['rows'][0]['elements'][0]['distance']['text']			
			print name1 , name2, t,d, "(%s,%s)"%(index1,index2)
			out.write("%s,\t%s,\t%s,\t%s\n"%(name1.decode("utf8") , name2.decode("utf8"), t,d))
			out.close()

