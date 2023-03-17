# Creating command line options
import re, argparse
import plistlib

# find duplicate values
def findDuplicates(fileName):
    print('Finding duplicates song in %s...' % fileName)
    # Read in the playlist
    # readPlist method takes a p-list file as input and 
    # return top level dictionary
    plist = plistlib.readPlist(fileName)
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
        plist = plistlib.readPlist(fileName)
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
    commonTracks = set.intersection)*trackNameSets)
    
    # write to file
    if len(commonTracks) > 0:
        f =open("common.txt", "w")
        for val in commonTracks:
            s = "%s\n" % val
            f.write(s.encode("UTF-8"))
        f.close()
        print("%d common tracks found. "
              "Track names written to common.txt." % len(commonTracks))
    else:
        print("Sorry, no tracks")

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