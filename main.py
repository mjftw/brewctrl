from brewctrl import TempCtrlAPI, TempCtrl, JsonConfig, SSEStream, W1TempSensor
from brewctrl.mocks import MockFileSensor, MockConfig, MockPower

if __name__ == '__main__':
    event_stream = SSEStream()
    TempCtrlAPI(
        event_stream=event_stream,
        tempctrl=TempCtrl(
            refresh_period_s=1,
            config=JsonConfig('settings.json'),
            temp_sensor=MockFileSensor('sensor_value'),
            hot_power=MockPower('Hot'),
            cold_power=MockPower('Cold'),
            event_stream=event_stream
        )
    ).start()