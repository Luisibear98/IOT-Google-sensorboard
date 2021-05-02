
# IOT-Google-sensorboard
This is repository for the final assignment. Its aim is to provide the code necessary to make the Google SensorBoard to work with an Rasberry pi 3B+.

The class board.py has been modified to access directly to the sensors as they were returning errors on the original program.


# Moisture sensor

For the aim of a final project, a moisture sensor has been added. To make it work, the idea is to connect an Arduino through the serial port to the rasberry.


#Final GCLOUD arquitecture


Finally, the rasberry will be sending the measurements to GCLOUD using the pub/sub protocol.
Take into account you MUST configure the cloud.init configuration file.


![Untitled Diagram (1)](https://user-images.githubusercontent.com/43785734/116818486-e3679980-ab6b-11eb-892a-22e0238bc7b8.png)
