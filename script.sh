#!/bin/bash

# SFTP Data Collector.This script can be used, if the source device/server is
# unable to "get" file recursively.Step in this script:
# To use password from environment set values for
#
# PASS_SRC for source.
# PASS_DEST for destination.
#
# 1. "get" listing of the files present.
# 2. select files required from the list using a reg_ex or a pattern. (currently this is yyyymmdd_hh)
# 3. Download select files.


export PASS_SRC=ahmed
export PASS_DEST=ahmed

# Below date yyymmdd_hh can be passed as a recurring value to run this script as a cron job daily/hourly
python sftp_data_collector.py -sh localhost -su ahmed -sp ahmed -dh localhost -du ahmed -dp ahmed -c src_dir -y dest_dir -p 20141013_-_13

# Password from ENV
#python sftp_data_collector.py -sh localhost -su ahmed -es -dh localhost -du ahmed -ed -c src_dir -y dest_dir -t 20141013_11 --debug


# Sample Date Range script below. yyymmddhhmm

#start_day_time=201410100000
#end_day_time=201410101000
#
#if [ "$start_day_time" -lt "$end_day_time" ]
#then
#    until [ "$start_day_time" -eq "$end_day_time" ]
#    do
#        inc_start_date_time=${start_day_time:0:8}' '${start_day_time:8:4}
#        inc_start_date_time_new=$(/bin/date --date "$inc_start_date_time +1 hour" +%Y%m%d\ %H%M)
#        start_day_time=${inc_start_date_time_new:0:8}${inc_start_date_time_new:9:4}
#
#        date_range=${inc_start_date_time:0:8}'_-_'${inc_start_date_time:9:2}
#        echo $date_range
#    done
#fi

