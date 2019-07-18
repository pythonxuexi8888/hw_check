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

# Start from here!
if [[ -z ${1} ]] || [[ -z ${2} ]] ; then
  echo "USAGE: ./find_diff.sh <TEMPLATE_FILE> <DIRECTORY>"
  exit 1
fi

TEMP=$1
DIR=$2

if [[ ! -d ${DIR} ]]; then
  red_echo "${DIR} is not a directory!"
  exit 1
fi

for filename in `ls ${DIR}`; do
  diff ${TEMP} ${DIR}/${filename} > /dev/null 2>&1
  if [[ "$?" != "0" ]]; then
    red_echo "${filename} is different from ${TEMP}!"
  else
    green_echo "${filename} is consistent with ${TEMP}!"
  fi
done
