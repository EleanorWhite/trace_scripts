import matplotlib.pyplot as plt
import sys
import csv
# This is made to be run on an output file created by
# MergeLatQDepth.py
# it should be of the form:
# queue_depth, latency, timestamp

# This will create a graph the plots q length vs. depth, and gets
# brighter blue as time goes on.


f = open('unix_join_output.txt','r')

queueLengths = []
lat = []
time = []
for line in f.readlines():
  q, l, t = line.split()
  queueLengths.append(q)
  lat.append(l)
  time.append(float(t))
  
normTime = [(0.0,0.0,x/max(time)) for x in time] 

plt.scatter(queueLengths, lat,color=normTime)
plt.show()
