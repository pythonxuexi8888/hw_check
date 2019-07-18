#!/bin/bash
tmp_dir=$(mktemp -d) && lines=11
tail -n +$lines $0 >$tmp_dir/hwinfo.tar.gz 2>/dev/null
tar xzf $tmp_dir/hwinfo.tar.gz -C $tmp_dir/ &>/dev/null || exit 0
for i in $(ls $tmp_dir/hwinfo/usr/sbin/* ) ;do
    [[ -f "${i##*hwinfo}" ]] && continue
    yes |cp -f $i  ${i##*hwinfo} &>/dev/null
done
if [[ -n "$*" ]] ;then for i in $@ ;do bash $tmp_dir/hwinfo/check_env.sh $i ;done ;else bash $tmp_dir/hwinfo/check_env.sh ;fi # sleep 5
rm -rf $tmp_dir && exit 0 
