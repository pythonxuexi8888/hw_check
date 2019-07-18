#!/bin/bash
report_file="hdd_report.csv"
[[ -f $report_file ]] && rm -f $report_file
touch $report_file

# disk_name partition_type divece_type product_model
lsblk -dn -o NAME,TYPE,ROTA,SIZE,MODEL |awk '\
/disk/{
	for(i=1;i<NF;i++)
	{
		if(i<5)
			printf("%s",$i",")
		else
		{
			if(i<NF)
				printf("%s ",$i)
		}
	}
	print $NF
}' >$report_file

#sed -i "1i device,type,rotabale,size,vendor,product_version" $report_file
sed -i "1i device,type,rotabale,size,product_version" $report_file
