import sys

perIOFilename = sys.argv[1]

latFile = open('latency.txt', 'w')
numBlocksFile = open('numBlocks.txt', 'w')


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





def getLatency():
    perIO = open(perIOFilename, 'r')
    
    latInfo = []
    nbinfo = []
    currentLineInfo = [] # [startTime, numBlocks]
    
    startTime = 0
    for line in perIO:
        l = parseLine(line)
        if(l == []):
            currentLineInfo = []
        elif (l != []):
            if l[1] == 'Q':
                startTime = l[0]
            if l[1] == 'C':
                lat = float(l[0]) - float(startTime)
                currentLineInfo.append(str(lat))
                
                # Poorly formatted way of saying "everything after the plus"
                # because the data comes in "blockNumber+NumberOfBlocks"
                # And we're extracting numberOfBlocks
                currentLineInfo.append(l[2][1+(l[2].index('+')):])
                #print(currentLineInfo)
                numBlocksFile.write(currentLineInfo[0] + ' ' + currentLineInfo[1] + '\n')
    #for i in latInfo:
    #    latFile.write(i[0] + " " + i[1] + "\n")
    #for i in nbinfo:
    #    numBlocksFile.write(str(i[0]) + ' ' + str(i[1]) + '\n')
    #    #latFile.write(str(startTime) + " " + str(lat) + "\n")

getLatency()

#def getNumBlocks():
#    perIO = open(perIOFilename, 'r')
#    for line in perIO:
#        l = parseLine(line)
#        if(l == []):
#            currentLineInfo = []
#        else:
#            if(l[1] == 'Q'):
#            if(l[1] == 'C'):
#                # Poorly formatted way of saying "everything after the plus"
#                # because the data comes in "blockNumber+NumberOfBlocks"
#                # And we're extracting numberOfBlocks
#                currentLineInfo.append(l[2][1+(l[2].index('+')):])
#                print(currentLineInfo)
#                info.append(currentLineInfo)
#    info = sorted(info, key= lambda e:float(e[0]))
#    for i in info:
#
