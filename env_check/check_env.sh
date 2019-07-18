#! /bin/bash

pkg_list="lshw pciutils nvme-cli"

_check_pkg(){
    lshw -version
    nvme --version
    #
}

if ! yum -y install $pkg_list &>/dev/null ;then
    echo "please get $pkg_list installed !"
    exit 1
fi

bash bin/check_cpu.sh
bash bin/check_mem.sh
bash bin/check_nic.sh
bash bin/check_hdd.sh
python bin/check_nvme.py
python bin/check_raid.py

bash bin/catcsv.sh  ./*.csv   #cpu_report.csv mem_report.csv nic_report.csv hdd_report.csv nvme_report.csv raid_report.csv

