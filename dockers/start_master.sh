#!/bin/bash
# Start rabbit on master
python3 master_job_signals.py &
python3 -m pulzarutils.dbupdater master
uwsgi -i config/master.ini
