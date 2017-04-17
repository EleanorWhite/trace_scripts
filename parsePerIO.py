#!/usr/bin/env python

# The functionality of the program is based on btt output
# btt is a program that parses blktrace
# to start using it, take all your blktrace files and run
# blkparse -i input_filenames -d output_file_name

import sys

perIOFilename = sys.argv[1]
BLOCK_NUMBERS = True

# This should be a file with perIO info
# you can create a file like this using the command:
# btt -i blkparse_file -p per_IO_filename
perIO = open(perIOFilename, 'r')

outputFile = open('genQDep', 'w')
latFile = open('latency.txt', 'w')


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
   
def getSortedEntries():
    ''' This creates a list of all the IO requests completed,
    each entry will be a list containing all the information in a line
    of the perIO input file. 
    It only includes data on when a request was queued and when it was
    completed. '''
    allEntries = []

    # add all useful lines to the entries
    for line in perIO:
        info = parseLine(line)
        if(not(info == [])):
            allEntries.append(info)

    sortedEntries = sorted(allEntries, key=lambda e:float(e[0]))
    # We only care about when data gets queued, and when it is completed.
    sortedEntries = [x for x in sortedEntries if x[1] == 'Q' or x[1] == 'C']

    return sortedEntries

 
def getQDep():
    sortedEntries = getSortedEntries()

    qDepInfo = []

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
        outputFile.write(i[0] + " " + i[1] + "\n")    

    #outputFile.write(str(entry[0]) + " " +  str(qLen) + "\n")


getQDep() 


def getLatency():
    perIO = open(perIOFilename, 'r')
    latInfo = []
    startTime = 0
    merged = False
    for line in perIO:
        l = parseLine(line)
        if (l != []):
            if l[1] == 'Q':
                startTime = l[0]
                blkno = l[2]
            if l[1] == 'M':
                merged = True
            if l[1] == 'C':
                lat = float(l[0]) - float(startTime)
                latInfo.append([str(startTime), str(lat),blkno, merged])
                merged = False
    latInfo = sorted(latInfo, key=lambda e:float(e[0]))
    for i in latInfo:
        if i[3]:
            latFile.write(i[0] + " " + i[1] + " " + i[2] + "\t" + "M" + "\n")
        else:
            latFile.write(i[0] + " " + i[1] + " " + i[2] + "\t" + "U" + "\n")
        #latFile.write(str(startTime) + " " + str(lat) + "\n")

getLatency()

