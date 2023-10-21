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
- `entries.json` [EDA notebook]()
	- `_id` — unique record identifier, {object};
	- `device` — sensor name {object}, categorical[5];
	- `noise` — sensor noise {integer}, categorical[4];
	- `sysTime` — {datetime}, matches `dateString`;
	- `dateString` — {datetime}, matches `sysTime`;
	- `rssi` — ??? {float}, constant;
	- `date` — ??? {float}, scientific notation;
	- __`sgv` — sensor glucose value in $mg/dL$ {float};__
	- `direction` — {object}, categorical[8] (allegedly predicts glucose change direction, needs to be verified);
	- `unfiltered` — Raw BG is calculated by applying the calibration to the glucose record's unfiltered value {float}, values distribution almost the same as `filtered`;
	- `filtered` — Raw BG is calculated by applying the calibration to the glucose record's filtered value. The glucose record's filtered values are generally produced by the CGM by a running average of the unfiltered values to produce a smoothed value when the sensor noise is high {float}, values distribution almost the same as `unfiltered`;
	- `type` — event type {object}, categorical[3];
	- `utcOffset` — time zone offset {integer}, constant;
	- `scale` — ??? {float}, constant, 99% missing;
	- `slope` — ??? {float}, 99% missing;
	- `intercept` — ??? {float}, 99% missing;
	- `mbg` — ??? {float}, 99% missing;
	- `trend` — ??? {float}, 99% missing;
	- `trendRate` — ??? {float}, constant, 99% missing;
- `treatments.json` [EDA notebook](https://github.com/WanomiR/cgm-analytics/blob/develop/src/notebooks/eda_treatments.ipynb)
	- `_id` —
	- `amount` — ??? {float};
	- `rate` — very similar to `absolute`
	- `timestamp` —
	- `enteredBy` —
	- `created_at` — 
	- `eventType` —
	- `duration` — duration ??? in allegedly in seconds {float};
	- `temp` —
	- `absolute` – very similar to `rate`
	- `utcOffset` — time zone offset {integer}, constant;
	- `carbDelayTime` — ??? {integer}, constant, >90% missing;
	- `carbs` — carbohydrates intake in grams {float}, >90% missing;
	- `dia` — insulin duration value (how much insulin is left active), defaults to 3 hours {float}, constant, >90% missing;
	- `insulinName` — >90% missing
	- `insulinPeak` — ??? {integer}, constant, >90% missing;
	- `insulinCurve` — >90% missing
	- `insulin` — insulin bolus, {float}, values distribution almost identical to `programmed`;
	- `insulinID` — >90% missing
	- `notes` — 99% missing
	- `glucose` — glucose value in $mmol/L$ {float}, 99% missing
	- `glucoseType` — 99% missing
	- `unabsorbed` — {integer}, constant;
	- `programmed` — insulin bolus, {float}, values distribution almost identical to `insulin`;
	- `type` —
	- `absorbtionTime` — >90% missing
	- `reason` — 99% missing
	- `correctionRange` — 99% missing
	- `insulinNeedsScaleFactor` — 99% missing
	- `automatic` —
	- `syncIdentifier` —
	- `userEnteredAt` — 99% missing
	- `foodType` — 99% missing
	- `userLastModifiedAt` — 99% missing