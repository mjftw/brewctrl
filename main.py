from brewctrl import TempCtrlAPI, TempCtrl, JsonStorage, SSEStream
from brewctrl.mocks import MockSensor, MockStorage, MockPower

if __name__ == '__main__':
    event_stream = SSEStream()
    TempCtrlAPI(
        event_stream=event_stream,
        tempctrl=TempCtrl(
            refresh_period_s=3,
            storage=MockStorage(),
            temp_sensor=MockSensor(),
            hot_power=MockPower('Hot'),
            cold_power=MockPower('Cold'),
            event_stream=event_stream
        )
    ).start()