import RPi.GPIO as GPIO
from time import sleep

ledpin = 35# PWM pin connected to LED
#GPIO.setwarnings(False)#disable warnings
GPIO.setmode(GPIO.BOARD)#set pin numbering system
GPIO.setup(ledpin,GPIO.OUT)
pi_pwm = GPIO.PWM(ledpin,6000)#create PWM instance with frequency
pi_pwm.start(0)#start PWM of required Duty Cycle 

while True:
        on_time_ms = 5
        pi_pwm.ChangeDutyCycle(100)
        sleep(on_time_ms/1e3)
        pi_pwm.ChangeDutyCycle(0)
        sleep((1/30)-(on_time_ms/1e3))