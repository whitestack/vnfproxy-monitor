

apt-get install lxd
lxd init

Do you want to configure a new storage pool (yes/no) [default=yes]?
Name of the storage backend to use (dir or zfs) [default=zfs]:
Create a new ZFS pool (yes/no) [default=yes]?
Name of the new ZFS pool or dataset [default=lxd]:
Would you like to use an existing block device (yes/no) [default=no]?
Size in GB of the new loop device (1GB minimum) [default=15]: 8
Would you like LXD to be available over the network (yes/no) [default=no]?
Do you want to configure the LXD bridge (yes/no) [default=yes]?
Warning: Stopping lxd.service, but it can still be activated by:
  lxd.socket
LXD has been successfully configured.


apt-get install juju
