# 9999-DD-2004 Test Setup

## Overview
This document outlines the hardware setup for testing the 9999-DD-2004 PCB.
The PCB is an electrical circuit that generates an analog output signal via PWM
control of an open drain digital pin. This analog signal drives an opto-isolator
output with an LC filter. Finally there is a set of SSRs, one NO and one NC, that
allow a signal to pass through unmodified or use the output of the PWM LC circuit.

## Schematic
![Schematic Diagram](9999-DD-2004.pdf)
