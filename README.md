# cephfs-autosnap

A tool designed to take snapshots of CephFS, both manual and automatic

Currently only manual snapshotting works

Supports both kernel CephFS mounts as well as CephFS fuse mounts

Creates snapshots based on linux path name rather than absolute CephFS path/dir name, so any snaps created on the root of the CephFS mount will have the name of the mounted directory

i.e if the CephFS directory is called CephFS, but mounted at /mnt/cephdirectory, the snapshots will inherit the name of cephdirectory-$time, instead of CephFS-$time
