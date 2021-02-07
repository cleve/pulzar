uwsgi -i config/volume.ini &
sleep 20
python3 job_discovery.py