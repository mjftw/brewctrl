from brewctrl import TempCtrlAPI, TempCtrl, JsonStorage
from brewctrl.mocks import MockSensor, MockStorage, MockPower

if __name__ == '__main__':
    TempCtrlAPI(
        tempctrl=TempCtrl(
            refresh_period_s=3,
            storage=JsonStorage('settings.json'),
            temp_sensor=MockSensor(),
            hot_power=MockPower(),
            cold_power=MockPower()
        )
    ).start()