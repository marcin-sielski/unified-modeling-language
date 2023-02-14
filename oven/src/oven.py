#!/usr/bin/env python3

"""
MIT License

Copyright (c) 2023 Marcin Sielski <marcin.sielski@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from enum import Enum
from time import sleep
from threading import Timer
import threading
import inspect
from playsound import playsound



class RepeatTimer(Timer):
    '''
    Repeats continuously scheduled routine

    Args:
        Timer (RepeatTimer): timer
    '''
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)



class OvenMode(Enum):
    '''
    Oven Mode

    Args:
        Enum (OvenMode): oven mode
    '''

    HOT_AIR = 1
    TOP_BOTTOM_HEATING = 2
    GRILL = 3



class OvenOption(Enum):
    '''
    Oven Option

    Args:
        Enum (OvenOption): oven option
    '''

    MODE = 1
    TEMPERATURE = 2
    TIME = 3



class OvenPanel:
    '''
    Oven Panel
    '''

    def __init__(self, parent):
        '''
        Initialize Oven Panel

        Args:
            parent (Oven): oven
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            type(self).__name__ + '.' + inspect.currentframe().f_code.co_name
        print(function_name)

        self.__parent = parent
        self.__option = OvenOption.MODE.value
        self.__mode = OvenMode.HOT_AIR.value
        self.__temperature = 150
        self.__timer_ok = Timer(5, self.button_ok)
        self.__hot = False
        self.__enabled = False
        self.__time = 20
        self.__timer_cancel = Timer(5, self.__cancel)
        self.__light_indicator = False


    def button_switch(self):
        '''
        Button Switch
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            type(self).__name__ + '.' + inspect.currentframe().f_code.co_name
        print(function_name)

        self.__enabled = not self.__enabled
        if not self.__enabled:
            self.__timer_ok.cancel()
            if self.__timer_ok.isAlive():
                self.__timer_ok.join()
            self.__timer_cancel.cancel()
            if self.__timer_cancel.isAlive():
                self.__timer_cancel.join()
            self.__parent.off()
            self.__init__(self.__parent)


    def button_up(self):
        '''
        Button Up
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            type(self).__name__ + '.' + inspect.currentframe().f_code.co_name
        print(function_name)

        if self.__enabled:
            if self.__option == OvenOption.TIME.value:
                self.__timer_cancel.cancel()
                if self.__timer_cancel.isAlive():
                    self.__timer_cancel.join()
                self.__timer_cancel = Timer(5, self.__cancel)
                self.__timer_cancel.name = 'TimerCancel'
                self.__timer_cancel.start()
                if self.__time < 180:
                    self.__time = self.__time + 10
            else:
                self.__timer_ok.cancel()
                if self.__timer_ok.isAlive():
                    self.__timer_ok.join()
                self.__timer_ok = Timer(5, self.button_ok)
                self.__timer_ok.name = 'TimerOk'
                self.__timer_ok.start()
                if self.__option == OvenOption.MODE.value and self.__mode < OvenMode.GRILL.value:
                    self.__mode = self.__mode + 1
                if self.__option == OvenOption.TEMPERATURE.value and self.__temperature < 250:
                    self.__temperature = self.__temperature + 5


    def button_down(self):
        '''
        Button Down
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            type(self).__name__ + '.' + inspect.currentframe().f_code.co_name
        print(function_name)

        if self.__enabled:
            if self.__option == OvenOption.TIME.value:
                self.__timer_cancel.cancel()
                if self.__timer_cancel.isAlive():
                    self.__timer_cancel.join()
                self.__timer_cancel = Timer(5, self.__cancel)
                self.__timer_cancel.name = 'TimerCancel'
                self.__timer_cancel.start()
                if self.__time > 20:
                    self.__time = self.__time - 10
            else:
                self.__timer_ok.cancel()
                if self.__timer_cancel.isAlive():
                    self.__timer_cancel.join()
                self.__timer_ok = Timer(5, self.button_ok)
                self.__timer_ok.name = 'TimerOk'
                self.__timer_ok.start()
                if self.__option == OvenOption.MODE.value and self.__mode > OvenMode.HOT_AIR.value:
                    self.__mode = self.__mode - 1
                if self.__option == OvenOption.TEMPERATURE.value and self.__temperature > 150:
                    self.__temperature = self.__temperature - 5


    def button_ok(self):
        '''
        Button Ok
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            type(self).__name__ + '.' + inspect.currentframe().f_code.co_name
        print(function_name)

        if self.__timer_ok.name != threading.currentThread().getName():
            self.__timer_ok.cancel()
            if self.__timer_ok.isAlive():
                self.__timer_ok.join()
        if self.__enabled:
            if self.__option == OvenOption.MODE.value:
                self.__option = OvenOption.TEMPERATURE.value
            elif self.__option == OvenOption.TEMPERATURE.value:
                self.__parent.start_heating(self.__mode, self.__temperature)
            else:
                self.__timer_cancel.cancel()
                if self.__timer_cancel.isAlive():
                    self.__timer_cancel.join()
                self.__parent.setup_time(self.__time)


    def button_clock(self):
        '''
        Button Clock
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            type(self).__name__ + '.' + inspect.currentframe().f_code.co_name
        print(function_name)

        if self.__enabled:
            self.__option = OvenOption.TIME.value


    def __cancel(self):
        '''
        Cancel
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            type(self).__name__ + '.' + inspect.currentframe().f_code.co_name
        print(function_name)

        self.__option = OvenOption.MODE.value


    def enable_light(self):
        '''
        Enable Light
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            type(self).__name__ + '.' + inspect.currentframe().f_code.co_name

        if not self.__light_indicator:
            self.__light_indicator = True
            print(function_name)


    def disable_light(self):
        '''
        Disable Light
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            type(self).__name__ + '.' + inspect.currentframe().f_code.co_name

        if self.__light_indicator:
            self.__light_indicator = False
            print(function_name)


    def __ring(self):
        '''
        Ring
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            type(self).__name__ + '.' + inspect.currentframe().f_code.co_name
        print(function_name)

        playsound('oven/snd/phone.wav')


    def hot(self):
        '''
        Hot
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            type(self).__name__ + '.' + inspect.currentframe().f_code.co_name

        if not self.__hot:
            print(function_name)
            self.__hot = True
            self.__ring()


    def ready(self):
        '''
        Ready
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            type(self).__name__ + '.' + inspect.currentframe().f_code.co_name
        print(function_name)

        for _ in range(5):
            self.__ring()



class Oven:
    '''
    Oven
    '''

    def __init__(self):
        '''
        Initialize Oven
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            type(self).__name__ + '.' + inspect.currentframe().f_code.co_name
        print(function_name)

        self.__panel = OvenPanel(self)
        self.__temperature = 0
        self.__temperature_target = 0
        self.__timer_heating = RepeatTimer(0.01, self.__heating)
        self.__timer_cooling = RepeatTimer(0.03, self.__cooling)
        self.__off = False
        self.__hot = False
        self.__schedule_heating = False
        self.__door_opened = False
        self.__time = 0
        self.__timer = Timer(self.__time, self.stop_heating)


    def off(self):
        '''
        Off
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            type(self).__name__ + '.' + inspect.currentframe().f_code.co_name
        print(function_name)

        self.__timer_heating.cancel()
        if self.__timer_heating.isAlive():
            self.__timer_heating.join()
        self.__timer_cooling.cancel()
        if self.__timer_cooling.isAlive():
            self.__timer_cooling.join()
        self.__off = True


    def __heating(self):
        '''
        Heating
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            type(self).__name__ + '.' + inspect.currentframe().f_code.co_name
        print(function_name + ':' + str(self.__temperature))

        if self.__temperature < 250 and self.__temperature < self.__temperature_target:
            self.__temperature = self.__temperature + 5
        if self.__temperature == self.__temperature_target:
            self.__panel.disable_light()
            self.__panel.hot()
            self.__hot = True


    def __cooling(self):
        '''
        Cooling
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            type(self).__name__ + '.' + inspect.currentframe().f_code.co_name
        print(function_name + ':' + str(self.__temperature))

        if self.__temperature > 0:
            self.__temperature = self.__temperature - 5
        if self.__temperature == 0 and self.__off:
            self.__timer_cooling.cancel()
            if self.__timer_cooling.isAlive():
                self.__timer_cooling.join()
            self.__init__()


    def start_heating(self, mode, temperature):
        '''
        Start heating

        Args:
            mode (OvenMode): oven mode
            temperature (int): temperature
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            type(self).__name__ + '.' + inspect.currentframe().f_code.co_name
        print(function_name + ':' + str(mode) + ',' + str(temperature))

        self.__panel.enable_light()
        self.__temperature_target = temperature
        self.__timer_heating.cancel()
        if self.__timer_heating.isAlive():
            self.__timer_heating.join()
        self.__timer_heating = RepeatTimer(1, self.__heating)
        self.__timer_heating.name = 'TimerHeating'
        self.__timer_heating.start()
        self.__timer_cooling.cancel()
        if self.__timer_cooling.isAlive():
            self.__timer_cooling.join()
        self.__timer_cooling = RepeatTimer(3, self.__cooling)
        self.__timer_cooling.name = 'TimerCooling'
        self.__timer_cooling.start()


    def stop_heating(self):
        '''
        Stop heating
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            type(self).__name__ + '.' + inspect.currentframe().f_code.co_name
        print(function_name)

        self.__timer_heating.cancel()
        if self.__timer_heating.isAlive():
            self.__timer_heating.join()
        self.__panel.ready()


    def door_open(self):
        '''
        Door Open
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            type(self).__name__ + '.' + inspect.currentframe().f_code.co_name
        print(function_name)

        if not self.__door_opened:
            self.__door_opened = True


    def door_close(self):
        '''
        Door Close
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            type(self).__name__ + '.' + inspect.currentframe().f_code.co_name
        print(function_name)

        if self.__door_opened:
            self.__door_opened = False
            if self.__schedule_heating:
                self.__timer = Timer(self.__time, self.stop_heating)
                self.__timer.name = 'Timer'
                self.__timer.start()


    def setup_time(self, time):
        '''
        Setup time

        Args:
            time (int): time
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            type(self).__name__ + '.' + inspect.currentframe().f_code.co_name
        print(function_name + ':' + str(time))

        self.__time = time
        if self.__hot:
            self.__timer = Timer(self.__time, self.stop_heating)
            self.__timer.name = 'Timer'
            self.__timer.start()
        else:
            self.__schedule_heating = True


    def get_panel(self):
        '''
        Gets Oven Panel

        Returns:
            OvenPanel: oven panel
        '''

        return self.__panel



class User:
    '''
    User
    '''

    @staticmethod
    def sequence_grill_ok_160_ok_heating():
        '''
        Scenario 1: select GRILL, temperature 160, start heating
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            inspect.currentframe().f_code.co_name
        print(function_name)

        oven = Oven()
        panel = oven.get_panel()
        panel.button_switch()
        panel.button_up()
        sleep(1)
        panel.button_up()
        sleep(1)
        panel.button_ok()
        panel.button_up()
        sleep(1)
        panel.button_up()
        sleep(1)
        panel.button_ok()
        sleep(60)

        assert (
            oven._Oven__temperature == 155 or oven._Oven__temperature == 160) and \
                oven._Oven__panel._OvenPanel__hot

        panel.button_switch()

        print(function_name + ': passed')


    @staticmethod
    def sequence_grill_ok_160_heating():
        '''
        Scenario 2: select GRILL, temperature 160, start heating
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            inspect.currentframe().f_code.co_name
        print(function_name)

        oven = Oven()
        panel = oven.get_panel()
        panel.button_switch()
        panel.button_up()
        sleep(1)
        panel.button_up()
        sleep(1)
        panel.button_ok()
        panel.button_up()
        sleep(1)
        panel.button_up()
        sleep(60)

        assert (oven._Oven__temperature == 155 or oven._Oven__temperature == 160) \
                and oven._Oven__panel._OvenPanel__hot

        panel.button_switch()

        print(function_name + ': passed')


    @staticmethod
    def sequence_hot_air_ok_160_heating():
        '''
        Scenario 3: select HOT_AIR, temperature 160, start heating
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            inspect.currentframe().f_code.co_name
        print(function_name)

        oven = Oven()
        panel = oven.get_panel()
        panel.button_switch()
        panel.button_up()
        sleep(1)
        panel.button_down()
        sleep(1)
        panel.button_ok()
        panel.button_up()
        sleep(1)
        panel.button_up()
        sleep(60)

        assert (oven._Oven__temperature == 155 or oven._Oven__temperature == 160) \
            and oven._Oven__panel._OvenPanel__hot

        panel.button_switch()

        print(function_name + ': passed')


    @staticmethod
    def sequence_grill_ok_160_timer_cancel():
        '''
        Scenario 4: select GRILL, temperature 160, setup timer, cancel
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            inspect.currentframe().f_code.co_name
        print(function_name)

        oven = Oven()
        panel = oven.get_panel()
        panel.button_switch()
        panel.button_up()
        sleep(1)
        panel.button_up()
        sleep(1)
        panel.button_ok()
        panel.button_up()
        sleep(1)
        panel.button_up()
        sleep(1)
        panel.button_clock()
        sleep(1)
        panel.button_up()
        sleep(10)

        assert oven._Oven__temperature == 0

        panel.button_switch()

        print(function_name + ': passed')


    @staticmethod
    def sequence_grill_ok_160_timer_heating():
        '''
        Scenario 5: select GRILL, temperature 160, setup timer, heating
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            inspect.currentframe().f_code.co_name
        print(function_name)

        oven = Oven()
        panel = oven.get_panel()
        panel.button_switch()
        panel.button_up()
        sleep(1)
        panel.button_up()
        sleep(1)
        panel.button_ok()
        panel.button_up()
        sleep(1)
        panel.button_up()
        sleep(1)
        panel.button_ok()
        panel.button_clock()
        sleep(1)
        panel.button_up()
        sleep(1)
        panel.button_ok()
        sleep(60)
        oven.door_open()
        oven.door_close()
        sleep(60)

        assert oven._Oven__temperature < 155 and oven._Oven__panel._OvenPanel__hot

        panel.button_switch()

        print(function_name + ': passed')


    @staticmethod
    def sequence_grill_ok_160_heating_timer():
        '''
        Scenario 6: select GRILL, temperature 160, heating, setup timer
        '''

        function_name = "'" + threading.currentThread().name + "'." + \
            inspect.currentframe().f_code.co_name
        print(function_name)

        oven = Oven()
        panel = oven.get_panel()
        panel.button_switch()
        panel.button_up()
        sleep(1)
        panel.button_up()
        sleep(1)
        panel.button_ok()
        panel.button_up()
        sleep(1)
        panel.button_up()
        sleep(1)
        panel.button_ok()
        sleep(60)
        panel.button_clock()
        sleep(1)
        panel.button_up()
        sleep(1)
        panel.button_ok()
        sleep(60)

        assert oven._Oven__temperature < 155 and oven._Oven__panel._OvenPanel__hot

        panel.button_switch()

        print(function_name + ': passed')



if __name__ == '__main__':

    threading.current_thread().name = 'User'

    try:
        User.sequence_grill_ok_160_ok_heating()
        User.sequence_grill_ok_160_heating()
        User.sequence_hot_air_ok_160_heating()
        User.sequence_grill_ok_160_timer_cancel()
        User.sequence_grill_ok_160_timer_heating()
        User.sequence_grill_ok_160_heating_timer()
    except AssertionError:
        print('Oven failure')
