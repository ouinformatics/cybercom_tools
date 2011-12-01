#!/bin/bash
# Location of the backup logfile.
logfile="/ddn_1/data/backups/dbs/postgres/logfile.log"
# Location to place backups.
backup_dir="/ddn_1/data/backups/dbs/postgres/data"
touch $logfile
timeslot=`date +%Y%m%d-%H%M`
databases=`psql -t -c "select datname from pg_database"`
#databases=`psql -h localhost -U postgres -q -c "\l" | sed -n 4,/\eof/p | grep -v rows\) | awk {'print $1'}`

for i in $databases; do
        timeinfo=`date '+%T %x'`
        echo "Backup and Vacuum complete at $timeinfo for time slot $timeslot on database: $i " >> $logfile
        /usr/bin/vacuumdb -z -h localhost -U postpres $i >/dev/null 2>&1
        /usr/bin/pg_dump $i -h 127.0.0.1 -U postgres | gzip > "$backup_dir/postgresql-$i-$timeslot-database.gz"
done
#-------------------------------------------------
