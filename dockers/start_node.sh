# Start rabbit on node
python3 register_job.py &
python3 -m pulzarutils.dbupdater volume
python3 job_discovery.py
uwsgi -i config/volume.ini