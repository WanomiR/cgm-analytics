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
3. Download the data from the most recent [`mongo_dump`](https://drive.google.com/drive/folders/1Lukvv8iPmfk3nX3-KrZ165xKgrmHeFw-?usp=share_link) and saved it under the `/src/data/` directory. It should look like this:

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

1. Navigate to the `/src` directory and run the main script.
	```bash
	$ cd src
	$ streamlit run Start.py
	```
