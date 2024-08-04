import requests

from models import GoveeDeviceResponse, GoveeStatusRequestPayload, GoveeStatusRequest, GoveeStatusResponse, InstanceType, HumidityValue

def farenheit_to_celsius(farenheit: float) -> float:
    return (farenheit - 32) * 5.0/9.0

def main():
    with open("govee_api_key.txt", "r") as f:
        api_key = f.read().strip()

    response = requests.get(
        f"https://openapi.api.govee.com/router/api/v1/user/devices",
        headers={"Content-Type": "application/json", "Govee-API-Key": api_key},
    )

    if response.status_code != requests.codes.ok:
        response.raise_for_status()

    govee_response = GoveeDeviceResponse.model_validate_json(response.text)

    for device in govee_response.data:
        print(device.device_name)

        payload = GoveeStatusRequestPayload(sku=device.sku, device=device.device)

        request = GoveeStatusRequest(
            payload=payload
        )

        data = request.model_dump(by_alias=True)

        response = requests.post(
            f"https://openapi.api.govee.com/router/api/v1/device/state",
            headers={"Content-Type": "application/json", "Govee-API-Key": api_key},
            json=data,
        )

        if response.status_code != requests.codes.ok:
            response.raise_for_status()

        govee_status_response = GoveeStatusResponse.model_validate_json(response.text)

        if govee_status_response.payload.capabilities is not None:
            for capability in govee_status_response.payload.capabilities:
                if capability.state is not None:
                    match capability.instance:
                        case InstanceType.ONLINE:
                            print(f"Online: {capability.state.value}")
                        case InstanceType.TEMPERATURE:
                            if isinstance(capability.state.value, float):
                                print(f"Temperature: {farenheit_to_celsius(capability.state.value):.1f} degrees")
                            else:
                                print("Cannot read temperature value")
                        case InstanceType.HUMIDITY:
                            if isinstance(capability.state.value, HumidityValue):
                                print(f"Value: {capability.state.value.current_humidity:.1f}%")
                            else:
                                print("Cannot read humidity value")
                        case _:
                            print(f"Value: {capability.state.value}")

        print()

if __name__ == "__main__":
    main()
