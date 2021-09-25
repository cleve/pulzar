# Start rabbit on node
python3 app/register_job.py -D
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start register_job: $status"
  exit $status
fi

python3 -m pulzarutils.dbupdater volume
python3 job_discovery.py
uwsgi -i config/volume.ini