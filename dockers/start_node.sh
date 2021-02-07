uwsgi -i config/master.ini &
sleep 20
python3 job_discovery.py