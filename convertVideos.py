#!/usr/bin/env python3
# Converts .h264 files into .mp4 files in a given folder

import sys
import os.path
from os import path
from subprocess  import call 

################################################################################
def convertFile(directoryPath, fileName):
    # Combines to get the full file path
    filePath = os.path.join(directoryPath, fileName)

    # Note that the MP4Box must be downloaded on your computer. I did a
    # 'brew install MP4Box' to get that working
    command = "MP4Box -add " + filePath + ' ' + filePath[:-4] + 'mp4'

    # Calls the command we crafted above
    call([command], shell=True)
    print('\tConverted', fileName, 'to an mp4.\n')

    # Remove the .h264 file once we're done converting it to .mp4
    os.remove(filePath)

################################################################################
def main():
    
    # Might be a more eloquent way to do this with getopts but I think this is
    # sufficient for my needs. No messing around.
    if len(sys.argv) != 2:
        print('Error: Wrong number of arguments. One argument is required - a valid path. Try using --help or -h if you are still having trouble formatting.')
        return

    # This argument should be a path to a directory or a cry for help in the
    # form of '--help' or '-h'
    argument = sys.argv[1]
    if argument == '--help' or argument == '-h':
        print('\nHelp:\tThis script takes the path to a directory as an argument. It will convert all the .h264 files in the directory to .mp4 files and then delete all .h264 files.\n\nFormat:\tpython convertVideos.py <path to directory>\n')
        return
    elif not path.exists(argument):
        print('Error: The path does not exist. Try again.')
        return
    elif not path.isdir(argument):
        print('Error: The path does not point to a directory. Try again.')
        return

    # Loop through all the files in the directory given
    for fileName in os.listdir(argument):
        if fileName.endswith(".h264"):
            # If there is an .h264 file, convert it
            convertFile(argument, fileName)
        else:
            # If it's anything else, do nothing
            continue


################################################################################
if __name__ == '__main__':
    main()

################################################################################