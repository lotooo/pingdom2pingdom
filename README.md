# pingdom2pingdom

Small app to hook pingdom app monitoring to pingdom server monitoring.
It will add markers to your scout dashboards during outage to help investigation (cross dashboard data)

## Usage

* With Docker :

```
sudo docker run -d -e SCOUTAPP_APIKEY=xxxxxxxxxxxx -p 5000:5000 lotooo/pingdom2pingdom
```

* Standalone app :
```
virtualenv -p python3.5 venv
source venv/bin/activate
pip install -r requirements.txt
export SCOUTAPP_APIKEY=xxxxxxxxxxxx
export FLASK_APP=pingdom2pingdom.py
flask run --host=0.0.0.0
```

## Debug

You can run the app with a specific env variables `FLASK_DEBUG=1` to enable debug logging.
