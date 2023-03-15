# Creating command line options
import re, argparse




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
    parse.add_argument('--dup', dest='plFileD', required=False)
    
    # parse args
    args = parser.parse_args()
    
    if args.plFiles:
        # find common track
        findCommonTracks(args.plFiles)
    elif args.plFile:
        # plot the tracks
        plotStats(args.plFile)
    elif args.plFileD:
        findDuplicates(args.plFiled)
    else:
        # if the user did not type any arguments
        print("These are not the track you are looking for")

# main method
if __name__ == '__main__':
    main()