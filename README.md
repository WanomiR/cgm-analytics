# App Instructions
How to run this app on macOS or Linux. 
1. Install Python in case you don't have it already. 
3. Open the project's root directory and create a virtual environment.
	```bash
	$ python -m venv venv
	```
3. Activate the environment, upgrade `pip`, and install dependencies.
	```bash
	$ source venv/bin/activate
	$ pip install --upgrade pip
	$ pip install -r requirements.txt
	```
3. Download the data from the most recent [`mongo_dump`](https://drive.google.com/drive/folders/1Lukvv8iPmfk3nX3-KrZ165xKgrmHeFw-?usp=share_link) and save it under the `/src/data/` directory. It should look like this:

	```
	src
	├── data
	│   ├── activity.json
	│   ├── devicestatus.json
	│   ├── entries.json
	│   ├── food.json
	│   ├── profile.json
	│   ├── settings.json
	│   └── treatments.json
	```

1. Navigate to the `/src` directory and run the main script `Start.py` with Streamlit.
	```bash
	$ cd src
	$ streamlit run Start.py
	```
# Data Dictionary
- `entries.json` [EDA notebook](https://github.com/WanomiR/cgm-analytics/blob/develop/src/notebooks/eda_entries.ipynb)
	- `_id` — unique record identifier, {object};
	- `device` — sensor name {object}, categorical[5];
	- `noise` — sensor noise {integer}, categorical[4];
	- `sysTime` — {datetime}, matches `dateString`;
	- `dateString` — {datetime}, matches `sysTime`;
	- `rssi` — ??? {float}, constant;
	- `date` — ??? {float}, scientific notation;
	- __`sgv` — glucose value in $mg/dL$, {float};__
	- `direction` — {object}, categorical[8] (allegedly predicts glucose change direction, needs to be verified);
	- `unfiltered` — ??? {float}, values distribution almost the same as `filtered`;
	- `filtered` — ??? {float}, values distribution almost the same as `unfiltered`;
	- `type` — event type {object}, categorical[3];
	- `utcOffset` — time zone offset {float}, constant;
	- `scale` — ??? {float}, constant, 99% missing;
	- `slope` — ??? {float}, 99% missing;
	- `intercept` — ??? {float}, 99% missing;
	- `mbg` — ??? {float}, 99% missing;
	- `trend` — ??? {float}, 99% missing;
	- `trendRate` — ??? {float}, constant, 99% missing;