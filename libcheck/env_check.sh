#! /bin/bash

function red_echo(){
  echo -e "\033[31m${1}\033[0m"
}

function green_echo(){
  echo -e "\033[32m${1}\033[0m"
}

function yellow_echo(){
  echo -e "\033[33m${1}\033[0m"
}

function blue_echo(){
  echo -e "\033[34m${1}\033[0m"
}


function check_ssh(){
  ssh root@${1} 'hostname' > /dev/null 2>&1
  if [[ "$?" != "0" ]]; then
    red_echo "${1}: Passwordless SSH Login Error"
  else
    green_echo "${1}: Passwordless SSH Login OK"
  fi
}

function install_packages(){
  ssh root@${1} 'yum install -y lshw pciutils nvme-cli' > /dev/null 2>&1
  if [[ "$?" != "0" ]]; then
    red_echo "${1}: Failed to install packages"
  else
    green_echo "${1}: Installed packages successfully"
  fi
}

function check_packages(){
  ssh root@${1} 'which lshw' > /dev/null 2>&1
  if [[ "$?" != "0" ]]; then
    red_echo "${1}: lshw not installed"
  else
    green_echo "${1}: lshw installed"
  fi
  ssh root@${1} 'which lspci' > /dev/null 2>&1
  if [[ "$?" != "0" ]]; then
    red_echo "${1}: pciutils not installed"
  else
    green_echo "${1}: pciutils installed"
  fi
  ssh root@${1} 'which nvme' > /dev/null 2>&1
  if [[ "$?" != "0" ]]; then
    red_echo "${1}: nvme-cli not installed"
  else
    green_echo "${1}: nvme-cli installed"
  fi
}

# Start from here!
if [[ -z ${1} ]] || [[ -z ${2} ]]; then
  echo "USAGE: ./os_env_check.sh <HOSTLIST> <type(ssh/install/package)>"
  exit 1
fi

HOSTLIST=${1}
TYPE=${2}

if [[ ! -f ${HOSTLIST} ]]; then
  red_echo "${HOSTLIST} doesn't exist!"
  exit 1
fi

if [[ "${TYPE}" != "ssh" ]] && [[ "${TYPE}" != "install" ]] && [[ "${TYPE}" != "package" ]]; then
  red_echo "Wrong Type!!"
  exit 1
fi

for HOST in `cat ${HOSTLIST}`; do
  if [[ -n "${HOST}" ]]; then
      case "${TYPE}" in
        "ssh")
          check_ssh ${HOST}
          ;;
        "install")
          install_packages ${HOST}
          ;;
        "package")
          check_packages ${HOST}
          ;;
      esac
  fi &
done
wait 
