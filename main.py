from brewctrl import TempCtrlAPI, TempCtrl, JsonStorage
from brewctrl.mocks import MockSensor, MockStorage, MockPower

if __name__ == '__main__':
    TempCtrlAPI(
        tempctrl=TempCtrl(
            refresh_period_s=3,
            storage=MockStorage(),
            temp_sensor=MockSensor(),
            hot_power=MockPower('Hot'),
            cold_power=MockPower('Cold')
        )
    ).start()