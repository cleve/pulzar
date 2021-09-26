#!/bin/bash
# Start rabbit on master
python3 master_job_signals.py -D
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start master_job_signals: $status"
  exit $status
fi

python3 -m pulzarutils.dbupdater master
uwsgi -i config/master.ini
