from energenie import switch_on, switch_off

class SmartPlugPower():
    ''' Eneregenie ENER010-PI smart plug power controller for RaspberryPi '''

    def __init__(self, socket):
        if socket not in [1, 2, 3, 4]:
            raise AttributeError('Socket must be in range 1-4')
        self.socket = socket

        self._is_on = None

        # Start off in known state
        self.off()

    def is_on(self):
        return self._is_on

    def on(self):
        switch_on(self.socket)
        self._is_on = True

    def off(self):
        switch_off(self.socket)
        self._is_on = False
