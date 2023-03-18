# Creating command line options
import re, argparse
import plistlib
from matplotlib import pyplot
import sys
import numpy as np

# find duplicate values
def findDuplicates(fileName):
    print('Finding duplicates song in %s...' % fileName)
    # Read in the playlist
    # readPlist method takes a p-list file as input and 
    # return top level dictionary
    with open(fileName, 'rb') as f:
        plist = plistlib.load(f)
    tracks = plist['Tracks']
    # create a track name dictionary
    trackNames = {}
    
    # loop through the tracks
    for trackId, track in tracks.items():
        try:
            name = track['Name']
            duration = track['Total Time']
            # look for existing entries
            if name in trackNames:
                # if a name and duration match, increment the count
                count = trackNames[name][1]
                trackNames[name] = (duration, count + 1)
            else:
                # add the new entry to the list
                trackNames[name] = (duration, 1)
        except:
            # ignore 
            pass
    # store duplicates as (name, count) tuples
    dups = []
    for k, v in trackNames.items():
        if v[1] > 1:
            dups.append((v[1],k))
    # save to a file
    if len(dups) > 0:
        print("Found %d duplicates. Track names saved to dups.txt" % len(dups))
    f = open("dups.txt", "w")
    for val in dups:
        f.write("[%d] %s\n" % (val[0], val[1]))
    f.close()    

# Find tracks common across multiple playlist

def findCommonTracks(fileNames):
    # a list of sets of tracks name
    trackNameSets = []
    for fileName in fileNames:
        # We create a new track
        trackNames = set()
        # read in the playlist
        with open(fileName, 'rb') as f:
            plist = plistlib.load(f)

        # get the track
        tracks = plist['Tracks']
        # loop through the tracks
        for trackId, track in tracks.items():
            try:
                # adding the trackname to a set
                trackNames.add(track['Name'])
            except:
                # ignore
                pass
        # add to list
        trackNameSets.append(trackNames)
    # get the set of common tracks
    commonTracks = set.intersection(*trackNameSets)
    
    # write to file
    if len(commonTracks) > 0:
        f =open("common.txt", "w")
        for val in commonTracks:
            s = "%s\n" % val
            f.write(s)
        f.close()
        print("%d common tracks found. "
              "Track names written to common.txt." % len(commonTracks))
    else:
        print("Sorry, no tracks")
# Collecting Statistics
def plotStats(fileName):
    # read in the playlist
    with open(fileName, 'rb') as f:
        plist = plistlib.load(f)

    
    # Getting tracks from the list
    tracks = plist['Tracks']
    # Creating lists of song rating and track durations
    ratings  = []
    durations = []
    # iterrate through the tracks
    for trackId, track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])
        except:
            # ignore the failing cases
            pass
    # ensure that valid data was collected
    if ratings == [] or durations ==[]:
        print("NO valid album rating or time data in %s" % fileName)
        return
    # plotting some data
    # scatter plot
    x = np.array(durations, np.int32) 
    # then, convert x into minutes
    x = x/60000.0
    y = np.array(ratings, np.int32)
    
    pyplot.subplot(2, 1, 1)
    pyplot.plot(x, y, 'o')
    pyplot.axis([0, 1.05*np.max(x), -1, 110])
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Track ratin')

    
    # plot histogram
    pyplot.subplot(2, 1, 2)
    pyplot.hist(x, bins=20)
    pyplot.xlabel('Track location')
    pyplot.ylabel('Count')
    
    # show plot
    pyplot.show()
def main():
    # We create the parser
    descStr="""
    This program analyzes playplist files (xml) exported from iTunes.
    """
    parser = argparse.ArgumentParser(description=descStr)
    # add a mutually exclusive group of arguments
    group = parser.add_mutually_exclusive_group()
    
    # add expected arguments: the values will be stored in dest: 
    # plFiles, PlFile, PlFiled
    parser.add_argument('--common', nargs='*', dest='plFiles', required=False)
    parser.add_argument('--stats', dest='plFile', required=False)
    parser.add_argument('--dup', dest='plFileD', required=False)
    
    # parse args
    args = parser.parse_args()
    
    if args.plFiles:
        # find common track
        findCommonTracks(args.plFiles)
    elif args.plFile:
        # plot the tracks
        plotStats(args.plFile)
    elif args.plFileD:
        findDuplicates(args.plFileD)
    else:
        # if the user did not type any arguments
        print("These are not the track you are looking for")

# main method
if __name__ == '__main__':
    main()