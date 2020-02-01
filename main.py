from TempCtrlAPI import TempCtrlAPI
from MockTempCtrl import MockTempCtrl

if __name__ == '__main__':
    TempCtrlAPI(MockTempCtrl()).start()