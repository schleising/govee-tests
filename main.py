import requests

from models import (
    GoveeDeviceResponse,
    GoveeStatusRequestPayload,
    GoveeStatusRequest,
    GoveeStatusResponse,
    InstanceType,
    HumidityValue,
)


# Function to convert Farenheit to Celsius
def farenheit_to_celsius(farenheit: float) -> float:
    return (farenheit - 32) * 5.0 / 9.0


def main():
    # Load the API key from a file
    with open("govee_api_key.txt", "r") as f:
        api_key = f.read().strip()

    # Get the list of devices associated with the API key
    response = requests.get(
        f"https://openapi.api.govee.com/router/api/v1/user/devices",
        headers={"Content-Type": "application/json", "Govee-API-Key": api_key},
    )

    # Check if the request was successful
    if response.status_code != requests.codes.ok:
        response.raise_for_status()

    # Parse the response into a GoveeDeviceResponse object
    govee_response = GoveeDeviceResponse.model_validate_json(response.text)

    # Iterate over the devices and print their names
    for device in govee_response.data:
        print(device.device_name)

        # Create a request to get the status of the device
        payload = GoveeStatusRequestPayload(sku=device.sku, device=device.device)
        request = GoveeStatusRequest(payload=payload)
        data = request.model_dump(by_alias=True)

        # Get the status of the device
        response = requests.post(
            f"https://openapi.api.govee.com/router/api/v1/device/state",
            headers={"Content-Type": "application/json", "Govee-API-Key": api_key},
            json=data,
        )

        # Check if the request was successful
        if response.status_code != requests.codes.ok:
            response.raise_for_status()

        # Parse the response into a GoveeStatusResponse object
        govee_status_response = GoveeStatusResponse.model_validate_json(response.text)

        # Print the capabilities of the device
        if govee_status_response.payload.capabilities is not None:
            for capability in govee_status_response.payload.capabilities:
                if capability.state is not None:
                    match capability.instance, capability.state.value:
                        case InstanceType.ONLINE, bool(online):
                            # Print the online status of the device
                            print(f"Online      : {online}")
                        case InstanceType.TEMPERATURE, float(temperature):
                            # Print the temperature in Celsius (converted from Fahrenheit)
                            print(
                                f"Temperature : {farenheit_to_celsius(temperature):.1f}°C"
                            )
                        case (
                            InstanceType.HUMIDITY,
                            HumidityValue(current_humidity=humidity),
                        ):
                            # Print the humidity value
                            print(f"Humidity    : {humidity:.1f}%")
                        case _:
                            # Print the value of the capability
                            print(f"Unknown value: {capability.state.value}")

        print()


if __name__ == "__main__":
    main()
