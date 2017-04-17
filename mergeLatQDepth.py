#!/usr/bin/env python
# The functionality of the program is based on btt output
# btt is a program that parses blktrace
# to start using it, take all your blktrace files and run
# blkparse -i input_filenames -d output_file_name

# Pass in the argument:
# filename_of_latency_file filename_of_queue_depth_file

import sys

# get filenames:
latFilename = sys.argv[1]
qFilename = sys.argv[2]
#print("latFilename:", latFilename, "qFilename", qFilename)

# This should be a file that has latency info from btt
# it will be of the form "time_of_io q2c_latency"
# you can create this with the command:
# btt -i blkparse_file -q lat.txt
# or you can make a more precise version using 
# parsePerIO.py
latFile = open(latFilename, 'r')

# This should be a file that has btt queue depth info
# it will be of the form "timestamp queue_depth_at_time"
# you can create this with the command:
# btt -i blkparse_file -Q qDepth
# or you can make a more precise version using 
# parsePerIO.py
depthFile = open(qFilename, 'r')

outputFile = open('output.txt', 'w')



def mergeLatDepth():
    ''' This takes two files containing btt latency and depth info
    and merges them into a file that has form "queue depth\t latency"
    '''
    # Adds a comment at the top with basic documentation
    outputFile.write("This file contains queue depth, latency, and time\
 information taken from btt\n")
    outputFile.write("Fields:\n")
    outputFile.write("depth_of_queue_when_request_is_made\
 time_between_request_made_and_completed\
 timestamp_when_request_is_made\n")

    
    depthFile = open(qFilename, 'r')
    # This is the queue length at a given time
    l = depthFile.readline()
    qdTime, qDepth = l.split() #depthFile.readline().split()
    
    
    for line in latFile:
        timestamp, latency, blkno = line.split()
 
        # Find the queue depth at the time of the beginning of the request
        while timestamp != qdTime:
            qdLine = depthFile.readline()
            if (not(qdLine == '')):
                qdTime,qDepth = qdLine.split()
            else:
                break
        if(qdTime == timestamp):
            #print (qDepth + "\t" + latency + "\t" + timestamp + "\n")
            outputFile.write(qDepth + "\t" + latency + "\t" + timestamp + "\t" + blkno + "\n")

mergeLatDepth()
