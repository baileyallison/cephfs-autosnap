#!/usr/bin/python3

#################################################################################
# CephFS-snapshots for taking CephFS-snapshots
# Linux/GNU License here
#################################################################################
from os import path
import subprocess
import re
import sys
from optparse import OptionParser


#################################################################################
# query to see if cephfs mounts exist
# checks for cephfs mounts, and exits if none are found
#################################################################################
##try to get this working without shell=true
def queryCephFSmounts():
    try:
        cephfsMountChecks = subprocess.check_output("df -PTh | awk '{print($7, $2)'} | grep ceph",shell=True, encoding='utf=8')
    except subprocess.CalledProcessError:
        do: sys.exit()
    else:
        pathToDirQuery=input("Path to CephFS dir where snapshots should be taken: ")
        df_pathtocephfs = subprocess.Popen(['df', '-PTh', pathToDirQuery], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        awk_for_ceph = subprocess.Popen(['awk', '{print $2}'], stdin=df_pathtocephfs.stdout, stdout=subprocess.PIPE, universal_newlines=True)
        df_pathtocephfs.stdout.close()
        is_it_ceph, err = awk_for_ceph.communicate()
        if "ceph" in is_it_ceph:
            dayTimeVar = subprocess.check_output(['date', '+%Y-%m-%d_%H%M%S'], universal_newlines=True).strip()
            if pathToDirQuery.endswith("/"):
                mkdir_snap = subprocess.check_output(['mkdir', f"{pathToDirQuery}"+'.snap/'+f"{pathToDirQuery.split('/')[-2]}"+f"-{dayTimeVar}"])
            elif pathToDirQuery.endswith(""):
                mkdir_snap = subprocess.Popen(['mkdir', f"{pathToDirQuery}"+'/.snap/'+f"{pathToDirQuery.rsplit('/')[-1]}"+f"-{dayTimeVar}"])
                print(pathToDirQuery.rsplit('/')[-1])
        elif "ceph" not in is_it_ceph:
            print("not a valid cephfs directory")
            do: sys.exit()

queryCephFSmounts()
###############################################################################
# manual cephfs snaps
###############################################################################

#################################################################################
# auto cephfs snaps
#################################################################################

##Auto Snapshots
##vars for auto snaps
#cephfsdir-snapvar -- path to cephfsdir to take auto snaps
#timetotake-var -- the time to take snaps - x mins,x hourly,x daily,x weekly,x yearly
#timetodelete-var -- the time to delete snaps - x mins,x hourly,x daily,x weekly,x yearly


################################################################################
# parses options, allows to create+edit+view snapshot tasks
################################################################################
def parsingArgs():
    parser = OptionParser() #use optparse to handle command line arguments
    parser.add_option('-c', '--create-snap', action="store_true",
		dest="createsnap", type="string", default=False, help="create snap on dir path")
    (options, args) = parser.parse_args()
## not ready
    #parser.add_option("-t", "--take-time", action="store_false",
	#	dest="take-time", default=True, help="take time of autosnaps")
    #parser.add_option("-k", "--keep-time", action="store_true", dest="keeptime",
	#	default=False, help="keep-time of autosnaps")
    #parser.add_option("-o", "--output", action="store_true", dest="output",
	#	default=False, help="output current active snapshot tasks")
if __name__ == "__parsingArgs__":
	parsingArgs()


#################################################################################
# options
#################################################################################
#def choose_output_header(options):
#	if no_output_flags(options):
#		return "Dev"
#	output = []
#	if options.createsnap:
#		do: queryCephFSmounts

## not ready
	#if options.taketime:
	#	option
	#if options.keeptime:
	#	option
#	return ",".join(output)

################################################################################
# function name: no_output_flags
# receives: options from parseOptions
# does: determines if no flags are passed for default output
# returns: True if default output, else False
################################################################################
#def no_output_flags(options):
#	return (not options.taketime and not options.keeptime
#			and not options.snap)

        
#################################################################################
# don't need this anymore
#################################################################################

# print list of found mounts -- not neccessary to print
# else:
#     cephfsMounts = cephfsMountChecks.replace(" ceph", "")
#     print (f"cephfs mounts are located at:\n{cephfsMounts}", end='')

## validation that ceph dir is ceph or not ceph -- not neccessary to print 
#        if "ceph" in is_it_ceph:
#            print("yes, good choice")
#        elif "ceph" not in is_it_ceph:
#            print("not a valid cephfs directory")
#            do: sys.exit()