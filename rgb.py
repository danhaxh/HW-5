import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Set button and LED pins
PB1 = 26
PB2 = 20
redPin = 12
greenPin = 19
bluePin = 13

# Set up buttons
GPIO.setup(PB1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PB2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up RGB LED
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)

# Set PWM frequency to 100 Hz
red_pwm = GPIO.PWM(redPin, 100)
green_pwm = GPIO.PWM(greenPin, 100)
blue_pwm = GPIO.PWM(bluePin, 100)

# Start with LED off
red_pwm.start(0)
green_pwm.start(0)
blue_pwm.start(0)

count = 0
flag = 0

try:
    while True:
        button1_state = GPIO.input(PB1)
        button2_state = GPIO.input(PB2)

        # PB2 turns off LED and resets count
        if button2_state == 0:
            red_pwm.ChangeDutyCycle(0)
            green_pwm.ChangeDutyCycle(0)
            blue_pwm.ChangeDutyCycle(0)
            count = 0

        # Count PB1 only once per press
        elif button1_state == 0 and flag == 0:
            count = count + 1

            # Fifth press returns to step 1
            if count > 4:
                count = 1

            if count == 1:
                red_pwm.ChangeDutyCycle(100)
                green_pwm.ChangeDutyCycle(0)
                blue_pwm.ChangeDutyCycle(0)
                print("Red - 100%")

            elif count == 2:
                red_pwm.ChangeDutyCycle(0)
                green_pwm.ChangeDutyCycle(0)
                blue_pwm.ChangeDutyCycle(75)
                print("Blue - 75%")

            elif count == 3:
                red_pwm.ChangeDutyCycle(50)
                green_pwm.ChangeDutyCycle(50)
                blue_pwm.ChangeDutyCycle(0)
                print("Yellow - 50%")

            elif count == 4:
                red_pwm.ChangeDutyCycle(0)
                green_pwm.ChangeDutyCycle(25)
                blue_pwm.ChangeDutyCycle(0)
                print("Green - 25%")

        # Remember whether PB1 is held or released
        if button1_state == 0:
            flag = 1
        else:
            flag = 0

        sleep(0.05)

except KeyboardInterrupt:
    print("Program stopped")

finally:
    red_pwm.stop()
    green_pwm.stop()
    blue_pwm.stop()
    GPIO.cleanup()
