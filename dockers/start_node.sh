#!/bin/bash
python3 k8s_settings.py
# Start rabbit on node
python3 register_job.py &
python3 -m pulzarutils.dbupdater volume
python3 job_discovery.py
uwsgi -i config/volume.ini