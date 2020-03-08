## how to run in development mode
```
./pull-covid-data.sh
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
python3 server.py
```

## Run in production with `waitress`
```
waitress-server server:app.server
```
