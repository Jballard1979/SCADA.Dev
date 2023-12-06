#!/usr/bin/env python3
#--
#-- ************************************************************************************************************:
#-- *********************************************** THM PSI SURGE **********************************************:
#-- ************************************************************************************************************:
#-- Author:   JBALLARD (JEB)                                                                                    :
#-- Date:     2023.3.07                                                                                         :
#-- Script:   THM-PSI.SURGE.MBTCP.py                                                                            :
#-- Purpose:  A python script to calc PSI Surges in a liquid Pipeline using inputs by polling MBTCP Registers.  :
#-- Version:  1.0                                                                                               :
#-- ************************************************************************************************************:
#-- ************************************************************************************************************:
#--
#-- ********************************************************:
#-- DEFINE PARAMS, CONSTANTS, CONFIG PATHS, IMPORT CLASSsES  :
#-- ********************************************************:
import time
import minimalmodbus
#--
# MBTCP CONNECTION PARAMETERS:
IP_ADDRESS = '10.165.3.40'
PORT = 502
SLAVE_ID = 1
#--
#-- MBTCP REG ADDRESSES:
PRESSURE_REG = 100
FLOW_RATE_REG = 101
PIPE_DIAMETER_REG = 102
PIPE_LENGTH_REG = 103
PIPE_ROUGHNESS_REG = 104
#--
#-- PIPELINE PROPERTIES:
pipeline_diameter = 0.0
pipeline_length = 0.0
pipeline_roughness = 0.0
#--
#-- MBTCP CONNECTION:
instrument = minimalmodbus.Instrument(IP_ADDRESS, SLAVE_ID)
instrument.serial.baudrate = 9600
instrument.serial.timeout = 1
instrument.address = SLAVE_ID
#--
#-- RETRIEVE PIPELINE PROPERTIES FROM MBTCP:
pipeline_diameter = instrument.read_register(PIPE_DIAMETER_REG)
pipeline_length = instrument.read_register(PIPE_LENGTH_REG)
pipeline_roughness = instrument.read_register(PIPE_ROUGHNESS_REG)
#--
#-- MAIN LOOP:
while True:
    try:
        #-- READ PSI & FLOW RATE FROM MBTCP:
        pressure = instrument.read_register(PRESSURE_REG)
        flow_rate = instrument.read_register(FLOW_RATE_REG)
        #--
        #-- CALC REYNOLDS:
        reynolds_number = 4 * flow_rate / (3.14159 * pipeline_diameter * 0.0001)

        #-- CALC FRICTION FACTOR:
        relative_roughness = pipeline_roughness / pipeline_diameter
        friction_factor = 64 / reynolds_number if reynolds_number < 2300 else 0.08 * relative_roughness ** (1 / 3)
        #--
        #-- CALC PSI DROP:
        velocity = flow_rate / (3.14159 * pipeline_diameter ** 2 / 4)
        pressure_drop = friction_factor * pipeline_length / pipeline_diameter * velocity ** 2 / 2
        #--
        #-- CALC PSI SURGE & CONVERT FROM kPa TO PSI:
        pressure_surge = pressure_drop / 1000 * 1.47
        #--
        #-- SHOW RESULTS:
        print('Pressure: {:.2f} kPa'.format(pressure))
        print('Flow rate: {:.2f} L/min'.format(flow_rate))
        print('Pressure surge: {:.2f} psi'.format(pressure_surge))
        #--
        #-- SLEEP:
        time.sleep(1)
    except Exception as e:
        print('Error:', e)
        break
#--
#-- ********************************************************:
#-- END OF SCRIPT                                           :
#-- ********************************************************: