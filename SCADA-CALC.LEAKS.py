#--
#-- ****************************************************************************************************************:
#-- ************************************************ CALCULATE LEAKS ***********************************************:
#-- ****************************************************************************************************************:
#-- Author:  JBallard (JEB)                                                                                         :
#-- Date:    2023.2.23                                                                                              :
#-- Script:  SCADA-CALC.LEAKS.py                                                                                    :
#-- Purpose: A python script that calculates leaks based off users input.                                           :
#-- Ver:     1.0                                                                                                    :
#-- ****************************************************************************************************************:
#-- ****************************************************************************************************************:
#--
#-- ********************************************************:
#-- DEFINE PARAMS, CONSTANTS, CONFIG PATHS, IMPORT CLASSES  :
#-- ********************************************************:
def CALC_LEAKS(volume, time):
    #--
    #-- CALCULATE LEAK:
    LKSPERSec    = volume / time
    LKSPERHour   = LKSPERSec * 3600
    LKSPERDay    = LKSPERHour * 24
    LKSPERYear   = LKSPERDay * 365
    #--
    return
    {
        "LKSPERSec": LKSPERSec,
        "LKSPERHour": LKSPERHour,
        "LKSPERDay": LKSPERDay,
        "LKSPERYear": LKSPERYear
    }
#--
#-- RETRIEVE USER INPUT:
volume = float(input("ENTER VOLUME OF LEAK USING LITERS: "))
time = int(input("ENTER TIME LEAK OCCURRED USING SECONDS: "))
#--
#-- CALL FUNCTION TO CALCULATE LEAKS:
leaks = CALC_LEAKS(volume, time)
#--
#-- PRINT LEAK RESULTS:
print(f"LEAK RATE: {leaks['LKSPERSec']:.2f} LITERS PER SECOND")
print(f"LEAK RATE: {leaks['LKSPERHour']:.2f} LITERS PER HOUR")
print(f"LEAK RATE: {leaks['LKSPERDay']:.2f} LITERS PER DAY")
print(f"LEAK RATE: {leaks['LKSPERYear']:.2f} LITERS PER YEAR")
#--
#-- ********************************************************:
#-- END OF SCRIPT                                           :
#-- ********************************************************: