#!/usr/bin/env python2.7

import subprocess
from subprocess import call

SDcard_threshold = 95  # % of SD card above which we'll delete the oldest .h264 files

def space_used():    # function displays amt of space left on device
    output_df = subprocess.Popen(["df", "-Ph"], stdout=subprocess.PIPE).communicate()[0]

    it_num = 0
    for line in output_df.split("\n"):
        line_list = line.split()
        if it_num == 1:
            storage = line_list
        it_num += 1
    print "Card size: %s Used: %s  Available: %s  Percent used: %s  SD Threshold: %d" % (storage[1], storage[2], storage[3], storage[4], SDcard_threshold)
    percent_used = int(storage[4][0:-1])
    if percent_used > SDcard_threshold:
        print "SD card %s full. Not enough space left! Removing oldest .h264 file" % storage[4]
        remove_a_file()  # call our function to make some space on the card
        space_used()     # call this function recursively until enough space on card

def practice():
    cmd = "stat --printf='%Y %n\0' /Users/blake/Desktop/*.txt" | sort -z | sed -zn '1s/[^ ]\{1,\} //p' |  xargs -0 rm"
    call('cmd', shell=True)
# from subprocess import call


###############################################################################
if __name__ == '__main__':
    space_used()
    practice()

###############################################################################