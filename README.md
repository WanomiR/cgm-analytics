# App Instructions
How to run this app on macOS or Linux.
1. Install Python in case you don't have it already.  
	Make sure that you downloaded the data and saved it under the `src/data/` directory.
1. Open the project's root directory and create a virtual environment.
	```bash
	$ python -m venv venv
	```
3. Activate the environment, upgrade `pip`, and install dependencies.
	```bash
	$ source venv/bin/activate
	$ pip install --upgrade pip
	$ pip install -r requirements.txt
	```
 4. Navigate to the `src` directory and run the main script.
	```bash
	$ cd src
	$ streamlit run Start.py
	```
