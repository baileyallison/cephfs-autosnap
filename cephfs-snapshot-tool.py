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
        cephfsMountChecks_df = subprocess.Popen(['df', '-PTh'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        cephfsMountChecks_awk = subprocess.Popen(['awk', '{print($7, $2)}'], stdin=cephfsMountChecks_df.stdout, stdout=subprocess.PIPE)
        cephfsMountChecks_grep = subprocess.Popen(['grep', 'ceph'], stdin=cephfsMountChecks_awk.stdout, stdout=subprocess.PIPE, universal_newlines=True)
        cephfsMountChecks_awk.stdout.close()
        mount_check, err = cephfsMountChecks_grep.communicate()
        if "ceph" not in mount_check:
            sys.exit()
    except subprocess.CalledProcessError:
        sys.exit()

queryCephFSmounts()


def pathofCephFS_snaps():
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
            mkdir_snap = subprocess.check_output(['mkdir', f"{pathToDirQuery}"+'/.snap/'+f"{pathToDirQuery.rsplit('/')[-1]}"+f"-{dayTimeVar}"])
            print(pathToDirQuery.rsplit('/')[-1])
    elif "ceph" not in is_it_ceph:
        print("not a valid cephfs directory")
        do: sys.exit()

pathofCephFS_snaps()
#################################################################################
# auto cephfs snaps
#################################################################################

##Auto Snapshots
##vars for auto snaps
#cephfsdir-snapvar -- path to cephfsdir to take auto snaps
#timetotake-var -- the time to take snaps - x mins,x hourly,x daily,x weekly,x yearly
#timetodelete-var -- the time to delete snaps - x mins,x hourly,x daily,x weekly,x yearly