import RPi.GPIO as GPIO
from time import sleep

ledpin = 35# PWM pin connected to LED
#GPIO.setwarnings(False)#disable warnings
GPIO.setmode(GPIO.BOARD)#set pin numbering system
GPIO.setup(ledpin,GPIO.OUT)
pi_pwm = GPIO.PWM(ledpin,1000)#create PWM instance with frequency
pi_pwm.start(0)#start PWM of required Duty Cycle 

while True:
    pi_pwm.ChangeDutyCycle(100)
   # sleep(0.008)
    sleep(1)
    pi_pwm.ChangeDutyCycle(0)
    #sleep(0.008)
    sleep(1)