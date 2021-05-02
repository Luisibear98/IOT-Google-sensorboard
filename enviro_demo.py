# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from coral.enviro.board import EnviroBoard
from coral.cloudiot.core import CloudIot
from luma.core.render import canvas
from PIL import ImageDraw
from time import sleep
import serial
import argparse
import itertools
import os
from csv import DictWriter
import datetime
import csv
import ast

DEFAULT_CONFIG_LOCATION = os.path.join(os.path.dirname(__file__), 'cloud_config.ini')


def update_display(display, msg):
    with canvas(display) as draw:
        draw.text((0, 0), msg, fill='white')


def _none_to_nan(val):
    return float('nan') if val is None else val



def looping_upload(args,enviro,arduino):
   
    with CloudIot(args.cloud_config) as cloud:      
         
         sensors = {}
         read_period = int(args.upload_delay / (2 * args.display_duration))
         
         for read_count in itertools.count():
              
              #Accessing temperature and humidity sensors and saving on the dictionary
              sensors['temperature'] =  round(enviro.temperature, 2)
              sensors['humidity'] =  round(enviro.humidity, 2)
              
              #Opening serial port to read arduino moisture sensor
              moisture = arduino.readline().decode('utf-8').rstrip()
              if moisture:
                 sensors['moisture'] = float(moisture)
              else: 
                 sensors['moisture'] = 0.0
              
              #Taking timestamp of the meassures
              utc = datetime.datetime.utcnow() 
              sensors['time'] = str(utc)
                
              #Accesing ambient and preassure sensors
              sensors['ambient_light'] =  round(enviro.ambient_light,2)
              sensors['pressure'] =  round(enviro.pressure,2)

              #Priting on OLED display
              msg = 'Temp: %.2f C\n' % _none_to_nan(sensors['temperature'])
              msg += 'RH: %.2f %%' % _none_to_nan(sensors['humidity'])
              
              update_display(enviro.display, msg)
              sleep(args.display_duration)
              
               
              msg = 'Light: %.2f lux\n' % _none_to_nan(sensors['ambient_light'])
              msg += 'Pressure: %.2f kPa' % _none_to_nan(sensors['pressure'])

              update_display(enviro.display,msg)
              sleep(args.display_duration)
              
              msg = 'Moisture: %.2f Mois\n' % _none_to_nan(sensors['ambient_light'])
              msg += 'Last time: ' + str(sensors['time']) +'\n'

                
              #Local backup on CSV  
              with open('event.csv', 'a') as f_object:
                  dictwriter_object = DictWriter(f_object, fieldnames=['temperature','humidity','moisture','time','ambient_light','pressure'])
                  dictwriter_object.writerow(sensors)
  
              f_object.close()

              update_display(enviro.display, msg)
              sleep(args.display_duration)
              # If time has elapsed, attempt cloud upload.
              if read_count % read_period == 0 and cloud.enabled():
                  cloud.publish_message(sensors)
    
        
 
def main():
    # Pull arguments from command line.
    parser = argparse.ArgumentParser(description='Enviro Kit Demo')
    parser.add_argument('--display_duration',
                        help='Measurement display duration (seconds)', type=int,
                        default=5)
    parser.add_argument('--upload_delay', help='Cloud upload delay (seconds)',
                        type=int, default=15)
    parser.add_argument(
        '--cloud_config', help='Cloud IoT config file', default=DEFAULT_CONFIG_LOCATION)
    args = parser.parse_args()

    # Create instances of EnviroKit and Cloud IoT.
    enviro = EnviroBoard()
    
    #Create instances for arduino
    arduino = serial.Serial('/dev/ttyACM0')
    
    #Executing the upload to gcloud function
    try:
        looping_upload(args,enviro,arduino)
    except:
        looping_upload(args,enviro,arduino)







if __name__ == '__main__':
    main()
