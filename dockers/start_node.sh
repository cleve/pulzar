uwsgi -i config/volume.ini &
sleep 5
python -m pulzarutils.dbupdater volume
python3 job_discovery.py