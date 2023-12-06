#--
#-- ************************************************************************************************************:
#-- ******************************************** SCADA LEAK LOCATION *******************************************:
#-- ************************************************************************************************************:
#-- Author:   JBALLARD (JEB)                                                                                    :
#-- Date:     2023.4.20                                                                                         :
#-- Script:   SCADA-LEAK.LOCATION.py                                                                            :
#-- Purpose:  A python script that calculates the Leak Location in a liquid Pipeline.                           :
#-- Version:  1.0                                                                                               :
#-- ************************************************************************************************************:
#-- ************************************************************************************************************:
#--
#-- ********************************************************:
#-- DEFINE PARAMS, CONSTANTS, CONFIG PATHS, IMPORT CLASSES  :
#-- ********************************************************:
import math
#--
def CALC_DIST(toa, SNDSpeed):
    return toa * SNDSpeed
#--
def CALC_LK_LOC(LKDist1, LKDist2, LKDistHt):
    return math.sqrt(LKDist1**2 - (LKDistHt**2)) - math.sqrt(LKDist2**2 - (LKDistHt**2))
#--
#-- CONFIGURE CLIENT:
MBTCPClient = ModbusTcpMBTCPClient('10.165.3.40', port=106671)
#--
#-- READ TOA SCADA DATA FROM PLC:
PLCRes1 = MBTCPClient.read_input_registers(address=0, count=1, unit=1)
PLCRes2 = MBTCPClient.read_input_registers(address=1, count=1, unit=1)
PLCToa1 = PLCRes1.registers[0]
PLCToa2 = PLCRes2.registers[0]
#--
#-- PROMPT USER FOR INPUT:
SNDSpeed = float(input("PLEASE ENTER THE SPEED OF SOUND IN THE LIQUID: "))
LKDistHt = float(input("PLEASE ENTER THE ELEVATION OF THE PIPELINE ABOVE THE GROUND: "))
#--
#-- CALC DISTANCES FROM SENSOR TO LEAK LOCATION:
LKDist1 = CALC_DIST(PLCToa1, SNDSpeed)
LKDist2 = CALC_DIST(PLCToa2, SNDSpeed)
#--
#-- CALC LEAK LOCATION:
LKLoc = CALC_LK_LOC(LKDist1, LKDist2, LKDistHt)
#--
#-- PRINT RESULTS:
print("THE SCADA LEAK LOCATION IS ", LKLoc, "METERS FROM SENSOR 1:")
#--
#-- CLOSE CLIENT CONNECTION:
MBTCPClient.close()
#--
#-- ********************************************************:
#-- END OF SCRIPT                                           :
#-- ********************************************************::