/*
 * C_PWM.c
 * 
 * Copyright 2024  <pi@raspberrypi>
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 * 
 * 
 */


/*
 Change the Intensity of LED using PWM on Raspberry Pi
 http://www.electronicwings.com
 */

#include <wiringPi.h>

#include <stdio.h>
#include <stdlib.h>

const int PWM_pin = 33;   /* GPIO 1 as per WiringPi, GPIO18 as per BCM */

int main (void)
{
  int intensity ;            

  if (wiringPiSetup () == -1)
    exit (1) ;

  pinMode (PWM_pin, PWM_OUTPUT) ; /* set PWM pin as output */

  while (1)
  {
	
    for (intensity = 0 ; intensity < 1024 ; ++intensity)
    {
      pwmWrite (PWM_pin, intensity) ;	/* provide PWM value for duty cycle */
      delay (1) ;
    }
    delay(1);

    for (intensity = 1023 ; intensity >= 0 ; --intensity)
    {
      pwmWrite (PWM_pin, intensity) ;
      delay (1) ;
    }
    delay(1);
}
}
