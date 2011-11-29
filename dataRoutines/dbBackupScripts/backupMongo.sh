#!/bin/bash
# Location to place backups.
timeslot=`date +%Y_%m_%d_%H%M`
backup_dir="/ddn_1/data/backups/dbs/mongo/$timeslot"
#make directory to backup mong
mkdir -p "$backup_dir"
touch "$backup_dir/log.txt"
#run mong backup
mongodump -h "localhost" -o "$backup_dir" >> "$backup_dir/log.txt" 2>&1
#-------------------------------------------------
