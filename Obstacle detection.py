import time
from espeak import espeak
import RPi.GPIO as GPIO

espeak.synth("Obstacle detection is started")


def read_distance():
    GPIO.setmode(GPIO.BCM)
    TRIG = 17
    ECHO = 27
    GPIO.setup(TRIG, GPIO.OUT)    
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, GPIO.LOW)

    # Send a HIGH signal to TRIG in order to trigger the sensor
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    # Record the pulse start time
    pulse_start = time.time()
    while GPIO.input(ECHO) != GPIO.HIGH:
        pulse_start = time.time()

    # Record the pulse end time
    pulse_end = pulse_start                 
    while time.time() < pulse_start + 0.1:
        if GPIO.input(ECHO) == GPIO.LOW:
            pulse_end = time.time()
            break

    GPIO.cleanup()

    pulse_duration = pulse_end - pulse_start
    distance = 34300 * pulse_duration / 2

    if distance > 400:
        return None
    return distance


if __name__ == '__main__':
    print ("Starting distance measurement! Press Ctrl+C to stop this script.")
    time.sleep(1)

    while True:
        # Track the current time so we an loop at regular intervals
        loop_start_time = time.time()

        # Read the distance and output the result
        distance = read_distance()
        if distance:
            print ("Distance: %.1f cm" % (distance))
            if distance <= 30:
                espeak.set_voice("en")
                
                espeak.synth("ALERT, Obstacle  NEAR")
                espeak.synth(str(round (distance,1)))
                
        time_to_wait = loop_start_time + 1 - time.time()
        if time_to_wait > 0:
            time.sleep(time_to_wait)
