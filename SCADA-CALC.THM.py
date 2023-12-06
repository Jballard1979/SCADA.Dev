#--
#-- ****************************************************************************************************************:
#-- ************************************************* CALCULATE THM ************************************************:
#-- ****************************************************************************************************************:
#-- Author:  JBallard (JEB)                                                                                         :
#-- Date:    2023.2.23                                                                                              :
#-- Script:  SCADA-CALC.THM.py                                                                                      :
#-- Purpose: A python script that calculates a Liquid Transient Hydraulic Model.                                    :
#-- Ver:     1.0                                                                                                    :
#-- ****************************************************************************************************************:
#-- ****************************************************************************************************************:
#--
#-- ********************************************************:
#-- DEFINE PARAMS, CONSTANTS, CONFIG PATHS, IMPORT CLASSES  :
#-- ********************************************************:
import numpy as np
import matplotlib.pyplot as plt
#--
length = 100.0               #-- Length of the pipe (in meters)
diameter = 0.1               #-- Diameter of the pipe (in meters)
density = 1000.0             #-- Density of the fluid (in kg/m^3)
viscosity = 0.001            #-- Viscosity of the fluid (in kg/m/s)
time_step = 0.01             #-- Time step for simulation (in seconds)
total_time = 10.0            #-- Total simulation time (in seconds)
initial_pressure = 100000.0  #-- Initial pressure (in Pa)
#--
#-- CREATE ARRAYS TO STORE DATA:
time = np.arange(0, total_time, time_step)
pressure = np.zeros(len(time))
pressure[0] = initial_pressure
#--
#-- SIMULATION LOOP:
for i in range(1, len(time)):
    #-- CALC CHANGE USING TRANSIENT FLOW EQUATION & REPLACE WITH USR PROVIDED EQUATION:
    pressure_change = ...
    #-- UPDATE PRESSURE FOR NEXT TIME STEP:
    pressure[i] = pressure[i - 1] + pressure_change
#--
#-- PLOT RESULTS:
plt.figure()
plt.plot(time, pressure)
plt.xlabel("Time (s)")
plt.ylabel("Pressure (Pa)")
plt.title("Transient Hydraulic Model")
plt.grid(True)
plt.show()
#--
#-- ********************************************************:
#-- END OF SCRIPT                                           :
#-- ********************************************************: