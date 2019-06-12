import numpy as np

obs_map = {"normal" : 0, "cold" : 1, "dizzy" : 2}
state_map = {"healthy" : 0, "fever" : 1}

pi = np.array([0.6, 0.4])

a = np.array([
    [0.7, 0.3],
    [0.4, 0.6]
])

b = np.array([
    [0.5, 0.4, 0.1],
    [0.1, 0.3, 0.6]
])

obs = [obs_map["normal"], obs_map["cold"]]
obs = [obs_map["normal"], obs_map["cold"], obs_map["dizzy"]]

#pi =[0.2,0.2,0.2,0.2,0.2]
#a = np.array([[7/15,3/15,3/15,0,2/15],
#	 [2/15,4/15,7/15,0,2/15],
#	 [4/15,7/15,2/15,0,2/15],
#	 [2/7,2/7,2/7,0,1/7],
#	 [0,0,0,0,0]
#])
#b = np.array([[4/10,3/10,2/10,1/10],
#	 [2/10,4/10,3/10,1/10],
#	 [2/10,2/10,5/10,1/10],
#	 [0,0,0,0],
#	 [0,0,0,0]
#])
#state_map = {'S1' : 0, 'S2':1,'S3':2,'BEGIN':3,'END':4}
#obs_map = {'RED' : 0, 'GREEN' : 1, 'BLUE' : 2,'UNK':3}
##state = ['S1','S2','S3','BEGIN','END']
##symbol = ['RED','GREEN','BLUE','UNK']
##pi = [0.2,0.2,0.2,0.2,0.2]
#obs = [obs_map["RED"], obs_map["RED"], obs_map["GREEN"],obs_map["BLUE"]]
##O = [0,0,1,2]