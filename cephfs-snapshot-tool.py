#!/usr/bin/env python3
#################################################################################
# cephfs-autosnap
# create and schedule cephfs snapshots on cephfs directories
# Copyright 2021, Bailey Allison <my-email-here@email.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#################################################################################
from os import path
import subprocess
import re
import sys
from optparse import OptionParser
import sched, time
import calendar
import datetime

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
            print("No CephFS mounts found")
            sys.exit()
    except subprocess.CalledProcessError:
        sys.exit()
queryCephFSmounts()

###################################################################################
# manual cephfs snapshots
###################################################################################
def pathofCephFS_snaps(options):
    pathToDirQuery=options.createsnap
    df_pathtocephfs = subprocess.Popen(['df', '-PTh', pathToDirQuery], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    awk_for_ceph = subprocess.Popen(['awk', '{print $2}'], stdin=df_pathtocephfs.stdout, stdout=subprocess.PIPE, universal_newlines=True)
    df_pathtocephfs.stdout.close()
    is_it_ceph, err = awk_for_ceph.communicate()
    if "ceph" in is_it_ceph:
        dayTimeVar = subprocess.check_output(['date', '+%Y-%m-%d_%H%M%S'], universal_newlines=True).strip()
        if pathToDirQuery.endswith("/"):
            mkdir_snap = subprocess.check_output(['mkdir', f"{pathToDirQuery}"+'.snap/'+f"{pathToDirQuery.split('/')[-2]}"+"-"+time.strftime("%Y-%m-%d_%H:%M:%S")])
            ## does not print correct path for visual feedback -- prints just the date
            print("Snapshot created:"+(pathToDirQuery.rsplit('/')[-2])+"-"+time.strftime("%Y-%m-%d_%H:%M:%S")+"at: "+f"{pathToDirQuery}"+".snap/")
        elif pathToDirQuery.endswith(""):
            mkdir_snap = subprocess.check_output(['mkdir', f"{pathToDirQuery}"+'/.snap/'+f"{pathToDirQuery.rsplit('/')[-1]}"+"-"+time.strftime("%Y-%m-%d_%H:%M:%S")])
            print("Snapshot created: "+(pathToDirQuery.rsplit('/')[-1])+"-"+time.strftime("%Y-%m-%d_%H:%M:%S")+"at: "+f"{pathToDirQuery}"+"/.snap/")
    elif "ceph" not in is_it_ceph:
        print("not a valid cephfs directory")
        do: sys.exit()

#################################################################################
# auto cephfs snaps
#################################################################################

##Auto Snapshots
##vars for auto snaps
#cephfsdir-snapvar -- path to cephfsdir to take auto snaps
#timetotake-var -- the time to take snaps - x mins,x hourly,x daily,x weekly,x yearly
#timetodelete-var -- the time to delete snaps - x mins,x hourly,x daily,x weekly,x yearly


##def scheduledcephfsSnaps(options):
##    datetime.datetime()
##    datetime.timedelta()


################################################################################
# parses options, allows to create+edit+view snapshot tasks
################################################################################
def main():
    parser = OptionParser()
    parser.add_option('-c', '--create-snap', action="store",
		dest="createsnap", default=False, help="create a snapshot on specified cephfs path", 
        metavar="/path/to/snapshot/dest/")
    parser.add_option('-s', '--schedule-snap', action="store_true",
		dest="schedulesnap", default=False, help="schedule a snapshot task on specified path",
        metavar="/path/to/snapshot/dest schedule-time-1d retention-time-1y")
    parser.add_option("-p", "--print", action="store_true",
        dest="print_task", default=False, help="print debug message for testing")
    (options, args) = parser.parse_args()
    
    if options.print_task:
        print("hello! you have found the task that let me figure out how parser works"+time.strftime("%Y-%m-%d_%H:%M:%S"))
    if options.createsnap:
        pathofCephFS_snaps(options)

if __name__ == "__main__":
	main()
#################################################################################
# options
#################################################################################
#def choose_output_header(options):
#	if no_output_flags(options):
#		return "Dev"
#	output = []
#	return ",".join(output)