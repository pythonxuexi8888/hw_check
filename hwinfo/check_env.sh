#!/bin/bash

#bash check_cpu.sh
#bash check_mem.sh
#bash check_nic.sh
#bash check_hdd.sh
#python check_nvme.py
#python check_raid.py

opt="cpu mem nic hdd nvme raid"

[[ -n $1 ]] && [[ ${opt//$1/} == $opt ]] && echo "unknown option \"$1\"" && exit 1
[[ -n $1 ]] && opt="$1"


pkg_list="lshw pciutils nvme-cli"

_check_pkg(){
    if lshw -version &>/dev/null && nvme --version &>/dev/null && lspci --version &>/dev/null ;then
        return 0
    elif yum -y install $pkg_list &>/dev/null ;then
        return 0
    else
        echo "please get $pkg_list installed !"
        exit 1
    fi
}

function _check_hw(){
    if [[ $1 == "nvme" ]] || [[ $1 == "raid" ]] ;then
        python $(dirname $0)/check_${1}.py
    else
        bash $(dirname $0)/check_${1}.sh
    fi
}

function _view_report(){
    bash $(dirname $0)/catcsv.sh  $(dirname $0)/$1*.csv   #cpu_report.csv mem_report.csv nic_report.csv hdd_report.csv nvme_report.csv raid_report.csv
}

if _check_pkg ;then
    for i in $opt ;do
        _check_hw $i
        _view_report $i
    done
fi

