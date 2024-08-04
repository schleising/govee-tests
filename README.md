# Read Govee Data

Reads Temperature and Humidity data from a Govee H5179 Temperature and Humidity sensor

## Usage

### Get an API Key
Apply for an API key using the instructions [here](https://developer.govee.com/reference/apply-you-govee-api-key), store the key in a file called `govee_api_key.txt` in the same directory as the script.

### Install the Dependencies

Install the required dependencies with the following command:

```bash
pip install -r requirements.txt
```

### Run the Script

Run the script with the following command:

```bash
python main.py
```

## Output

The script will output the temperature and humidity data to the console.

```bash
Bedroom Thermometer
Online      : True
Temperature : 21.1°C
Humidity    : 62.0%

Office Thermometer
Online      : True
Temperature : 21.7°C
Humidity    : 57.0%
```
