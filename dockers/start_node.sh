python3 -m pulzarutils.dbupdater volume
uwsgi -i config/volume.ini
python3 job_discovery.py