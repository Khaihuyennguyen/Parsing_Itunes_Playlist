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
    
    # add expected arguments
    parser.add_argument('--common', nargs='*', dest='plFiles', required=False)