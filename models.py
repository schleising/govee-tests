from enum import Enum

from pydantic import BaseModel, Field

class InstanceType(str, Enum):
    ONLINE = "online"
    TEMPERATURE = "sensorTemperature"
    HUMIDITY = "sensorHumidity"


class HumidityValue(BaseModel):
    current_humidity: float = Field(alias="currentHumidity")

class State(BaseModel):
    value: float | bool | HumidityValue

class Capability(BaseModel):
    type: str
    instance: InstanceType
    state: State | None = None

class Device(BaseModel):
    sku: str
    device: str
    device_name: str = Field(alias="deviceName")
    type: str
    capabilities: list[Capability]

class GoveeDeviceResponse(BaseModel):
    code: int
    message: str
    data: list[Device]

class GoveeStatusRequestPayload(BaseModel):
    sku: str
    device: str
    capabilities: list[Capability] | None = None

class GoveeStatusRequest(BaseModel):
    request_id: str = Field(default="uuid", alias="requestId")
    payload: GoveeStatusRequestPayload

class GoveeStatusResponse(BaseModel):
    request_id: str = Field(alias="requestId")
    code: int
    msg: str
    payload: GoveeStatusRequestPayload
