#!/usr/bin/env python




# The functionality of the program is based on btt output
# btt is a program that parses blktrace
# to start using it, take all your blktrace files and run
# blkparse -i input_filenames -d output_file_name

import sys

#perIO_fnameFilename = sys.argv[1]
BLOCK_NUMBERS = True

# This should be a file with perIO_fname info
# you can create a file like this using the command:
# btt -i blkparse_file -p per_IO_filename
#perIO_fname = open(perIOFilename, 'r')

#q_length_fname = open('genQDep', 'w')
#latFile = open('latency.txt', 'w')

# helper function
def parseLine(string):
    ''' Takes in a line of perio btt output and parses into a list of form
    (timestamp, action, blocknumber)
    returns an empty list if there is no info ''' 
    # different processes in the file are separated by lines of '-'s
    if (string[0:5] == '-----' or string == '\n' or string[0] == '#'):
        return []
    else:
        resultsArr = string.split()

        # the first line of data will contain the drive number before 
        # the other data. We don't care about that, so we drop it.
        if resultsArr[1] == ':':
            resultsArr = resultsArr[2:]
        return resultsArr
   
# helper function
def getSortedEntries(perIO_fname):
    ''' This creates a list of all the IO requests completed,
    each entry will be a list containing all the information in a line
    of the perIO_fname input file. 
    It only includes data on when a request was queued and when it was
    completed. '''
    allEntries = []
    perIO_file = open(perIO_fname, 'r')
    
    # add all useful lines to the entries
    for line in perIO_file:
        info = parseLine(line)
        if(not(info == [])):
            allEntries.append(info)

    sortedEntries = sorted(allEntries, key=lambda e:float(e[0]))
    # We only care about when data gets queued, and when it is completed.
    sortedEntries = [x for x in sortedEntries if x[1] == 'Q' or x[1] == 'C']

    return sortedEntries

 
def getQDep(perIO_fname, q_length_fname):
    """ This function creates a file with the queue depth at all given 
    timestamps. Puts this file with the filename q_length_fname"""
   
    q_length_file = open(q_length_fname, 'w')
    print "q length fname", q_length_fname 
    sortedEntries = getSortedEntries(perIO_fname)

    qDepInfo = []

    # print headers!
    q_length_file.write("timestamp\tqueue_length\n")

    qLen = 0
    firstFlag = True # this is true only the first time through the loop
    for entry in sortedEntries:
        if entry[1] == 'Q':
            qLen += 1
        elif entry[1] == 'C':
            qLen -= 1
        else:
            print("One of the entries is invalid. Please check input")
        qDepInfo.append([str(entry[0]), str(qLen)])
    qDepInfo = sorted(qDepInfo, key=lambda e:float(e[0]))
    for i in qDepInfo:
        q_length_file.write(i[0] + " " + i[1] + "\n")    

    #q_length_fname.write(str(entry[0]) + " " +  str(qLen) + "\n")


#getQDep() 


def getLatency(lat_fname, perIO_fname):
    """ This creates a file with the latency and request time """
    latFile = open(lat_fname, 'w')
    print "latFile", lat_fname
    perIO_file = open(perIO_fname, 'r')
    latInfo = []
    startTime = 0
    merged = False
    # print headers!
    latFile.write("start_time\tQ2C_latency\tD2C_latency\tblock_number\tmerged\n")

    for line in perIO_file:
        l = parseLine(line)
        if (l != []):
            if l[1] == 'Q':
                startTime = l[0]
                blkno = l[2]
            if l[1] == 'M':
                merged = True
            if l[1] == 'G':
                allocTime = l[0]
            if l[1] == 'I':
                insertTime = l[0]
            if l[1] == 'D':
                issueTime = l[0]            
            if l[1] == 'C':
                Q2C = float(l[0]) - float(startTime)
                D2C = float(l[0]) - float(issueTime)
                latInfo.append([startTime, str(Q2C),str(D2C), blkno, merged])
                merged = False
    latInfo = sorted(latInfo, key=lambda e:float(e[0]))
    for i in latInfo:
        if i[3]:
            latFile.write(i[0] + "\t" + i[1] + "\t" + i[2] + "\t" + i[3] + "\t" + "M" + "\n")
        else:
            latFile.write(i[0] + "\t" + i[1] + "\t" + i[2] + "\t" + i[3] + "\t" + "U" + "\n")
        #latFile.write(str(startTime) + " " + str(lat) + "\n")

"""
Official theory on the trace types in perIO:
Q: request is queued
G: request is allocated
I: inserted into the devices queue
D: request is issued to device
M: request is merged
C: request is completed
"""

#getLatency()


def main():
    if len(sys.argv) == 1:
        print "Usage: python parsePerIO.py -f <per_io_filename> -l <latency_output_filename> -q <q_depth_output_filename>"
    q = False
    f = False   
 
    perIO_fname = ""

    # parse command line args!
    for i in range(len(sys.argv)):
        if sys.argv[i] == "-i":
            perIO_fname = sys.argv[i+1]
        if sys.argv[i] == "-q":
            q = True
            q_length_fname = sys.argv[i+1]
        if sys.argv[i] == "-f":
            f = True
            lat_fname = sys.argv[i+1]
   
    if perIO_fname == "":
        print "Please enter perIO filename"     

    if f:
        getQDep(perIO_fname, q_length_fname)
    if q:
        getLatency(lat_fname, perIO_fname)







if __name__ == "__main__":
    main()
