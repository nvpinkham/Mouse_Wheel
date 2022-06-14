# python3
"""
Module to monitor the sensor on a mouse cage and detect when the
exercise wheel is in motion.
"""
import os
import sys
import gpiozero
from time import sleep, perf_counter
import datetime


SENSOR_PIN = 3  # GPIO3 on Raspi4

class WheelSensor():
    def __init__(self, pin_no: int):
        self._count = 0
        self._last_press_time = perf_counter()
        self._rpm = 0
        self._press_times = []
        self._pin = gpiozero.Button(pin_no, pull_up=True)
        self._pin.when_pressed = self._on_press
    #end def
        
        
    def _on_press(self):
        now = perf_counter()
        time_since_last_press = now - self._last_press_time
        self._last_press_time = now
        self._press_times.append(time_since_last_press)
        self._count += 1
        # print(f'Press count = {self._count}')
    #end def
        
        
    def reset_count(self):
        self._count = 0
    #end def
        
        
    def sensor_state(self) -> bool:
        return self._pin.value
    #end def
    
    def now(self):
        return self.now
    #end def
    
    @property
    def count(self) -> int:
        return self._count
    #end if
    
    
    @property
    def press_times(self) -> list:
        return self._press_times
    #end def
    
    
    @property
    def rpm(self) -> float:
        rpm = 60 / self._press_times[-1] if self._press_times else 0
        return rpm
    #end def
    
    @property
    def now(self) -> float:
        now = datetime.datetime.now()
        return now
    #end def
        
#end class

def do_monitor_mouse_wheel():
    
    print('Starting mouse wheel monitor')
    
    # the sensor is connected to GPIO1
    wheel_sensor = WheelSensor(SENSOR_PIN)
    prevcount = 0
    when_last_checked = datetime.datetime.now() - datetime.timedelta(0, 100)# make sure first pic is taken; if mouse hops on right away

    while True:
        #print(f'Sensor state = {wheel_sensor.sensor_state()}')
        sleep(.5)
        #print(f'{wheel_sensor.count} {wheel_sensor.now}')
        
        # print("Current", wheel_sensor.count)
        # print("Previous", prevcount)
        
        if(prevcount != wheel_sensor.count):
            
            print(f'{wheel_sensor.count} {wheel_sensor.now}')

            
            tdiff = datetime.datetime.now() - when_last_checked
            when_last_checked = datetime.datetime.now()

            #print(tdiff)
            
            if(tdiff > datetime.timedelta(0, 2)):
            
                print("smile you're on camera")
                os.system('raspistill -ex night -w 640 -h 480 -n -t 1000 -o pics/'+ str(wheel_sensor.count) + 'new_spin.jpg')
                
            if(wheel_sensor.count % 100 == 0):
            
                 print("smile you're on camera")
                 os.system('raspistill -ex night -w 640 -h 480 -n -t 1000 -o pics/'+ str(wheel_sensor.count) + 'Interval.jpg')    

            else:
                print("thinking its the same mouse")
            
            
        prevcount = wheel_sensor.count
    #end while
#end def


try:
    do_monitor_mouse_wheel()
except KeyboardInterrupt:
    print("STOPPED")
    raise SystemExit
    
