from brewctrl import TempCtrlAPI, TempCtrl
from brewctrl.mocks import MockSensor, MockStorage

if __name__ == '__main__':
    TempCtrlAPI(
        tempctrl=TempCtrl(
            storage=MockStorage(),
            temp_sensor=MockSensor()
        )
    ).start()