#!/usr/local/bin/python3

####
####CephFS-snapshots for taking CephFS-snapshots
##Linux/GNU License here
####Is titles
##Is comments/notes

from os import path
import subprocess
import re
import sys
from optparse import OptionParser

#################################################################################
# query to see if cephfs mounts exist
#################################################################################

####checks for cephfs mounts, and exits if none are found
try:
##try to get this working without shell=true
    cephfsMountChecks = subprocess.check_output("df -PTh | awk '{print($7, $2)'} | grep ceph",shell=True, encoding='utf=8')
##if no mounts are found exit
except subprocess.CalledProcessError:
    print("no cephfs mounts found")
##print list of found mounts
else:
    cephfsMounts = cephfsMountChecks.replace(" ceph", "")
    print (f"cephfs mounts are located at:\n{cephfsMounts}", end='')

####Where would you like your ceph snapshot(s) to be
##query where user would like snapshot(s) to be taken
    pathToDirQuery=input("Path to CephFS dir where snapshots should be taken: ")
    #pathToDirVar = str(pathToDirQuery)
    df_pathtocephfs = subprocess.Popen(['df', '-PTh', pathToDirQuery], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    awk_for_ceph = subprocess.Popen(['awk', '{print $2}'], stdin=df_pathtocephfs.stdout, stdout=subprocess.PIPE, universal_newlines=True)
    df_pathtocephfs.stdout.close()
    is_it_ceph, err = awk_for_ceph.communicate()
##if cephfs directory validate
    if "ceph" in is_it_ceph:
        print("yes, good choice")
##if not cephfs dir validate
    elif "ceph" not in is_it_ceph:
        print("not a valid cephfs directory")
        do: sys.exit()

###############################################################################
# manual cephfs snaps
###############################################################################

####What would you like your snapshot task(s) to be
##Manual Snapshots
    dayTimeVar = subprocess.check_output(['date', '+%Y-%m-%d_%H%M%S'], universal_newlines=True).strip()
    if pathToDirQuery.endswith("/"):
        #p2dvr = re.search('/(.*)/', pathToDirVar)
        mkdir_snap = subprocess.check_output(['mkdir', f"{pathToDirQuery}"+'.snap/'+f"{pathToDirQuery.split('/')[-2]}"+f"-{dayTimeVar}"])
    elif pathToDirQuery.endswith(""):
        mkdir_snap = subprocess.Popen(['mkdir', f"{pathToDirQuery}"+'/.snap/'+f"{pathToDirQuery.rsplit('/')[-1]}"+f"-{dayTimeVar}"])
        print(pathToDirQuery.rsplit('/')[-1])

#################################################################################
# auto cephfs snaps
#################################################################################

##Auto Snapshots
##vars for auto snaps
#cephfsdir-snapvar -- path to cephfsdir to take auto snaps
#timetotake-var -- the time to take snaps - x mins,x hourly,x daily,x weekly,x yearly
#timetodelete-var -- the time to delete snaps - x mins,x hourly,x daily,x weekly,x yearly


################################################################################
# function name: main
# receives: nothing
# does: parses CLI options, allows to create+edit+view snapshot tasks
# returns: 0 (success)
################################################################################
def main():
	parser = OptionParser() #use optparse to handle command line arguments
	parser.add_option("-c", "--create-snap", action="store_true",
			dest="snap", default=False, help="create snap on dir")
	parser.add_option("-t", "--take-time", action="store_false",
			dest="take-time", default=True, help="take time of autosnaps")
	parser.add_option("-k", "--keep-time", action="store_true", dest="keep-time",
			default=False, help="keep-time of autosnaps")
	parser.add_option("-o", "--output", action="store_true", dest="output",
			default=False, help="output current active snapshot tasks")        
    #parser.add_option("-h", "--help", action="store_true", dest="help",
	#		default=False, help="output options for command")
	(options, args) = parser.parse_args()

##################################################################################
# example of parser.add_option
##################################################################################
	#parser.add_option("-m", "--model", action="store_true", dest="outputModel",
	#		default=False, help="Output model names")