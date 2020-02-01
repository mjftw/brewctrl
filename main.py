from brewctrl import TempCtrlAPI, TempCtrl, JsonStorage
from brewctrl.mocks import MockSensor, MockStorage

if __name__ == '__main__':
    TempCtrlAPI(
        tempctrl=TempCtrl(
            storage=JsonStorage('settings.json'),
            temp_sensor=MockSensor()
        )
    ).start()