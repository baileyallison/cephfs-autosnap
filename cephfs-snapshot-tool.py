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


################################################################################
# parses options, allows to create+edit+view snapshot tasks
################################################################################
def main():
    parser = OptionParser() #use optparse to handle command line arguments
    parser.add_option('-c', '--create-snap', action="store_true",
		dest="createsnap", type="string", default=False, help="create snap on dir path")
    parser.add_option("-p", "--print", action="store_true",
        dest="print_task", type="string", default=False, help="print debug message")
    (options, args) = parser.parse_args()

if __name__ == "__main__":
	main()

## not ready
    #parser.add_option("-t", "--take-time", action="store_false",
	#	dest="take-time", default=True, help="take time of autosnaps")
    #parser.add_option("-k", "--keep-time", action="store_true", dest="keeptime",
	#	default=False, help="keep-time of autosnaps")
    #parser.add_option("-o", "--output", action="store_true", dest="output",
	#	default=False, help="output current active snapshot tasks")


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