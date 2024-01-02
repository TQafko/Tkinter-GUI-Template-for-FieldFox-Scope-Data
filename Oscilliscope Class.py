# Data retriver software using FieldFox Microwave Analyzer
# Author: Tedi Qafko
# Date: October 27 2023
# Commands Manual for SCPI commands of FieldFox:
# https://www.cmc.ca/wp-content/uploads/2020/06/SCPI_FFProgrammingHelp_20dec2018.pdf

import pyvisa
import numpy as np
import matplotlib.pyplot as plt

class FieldFoxScope:
    def __init__(self, centFreq, spanFreq, numPoints=401, debug=True):
        self.debug = debug
        self.numPoints = numPoints
        self.centFreq = centFreq
        self.spanFreq = spanFreq
        self.max_power = 0
        self.rm = pyvisa.ResourceManager()
        self.inst = self.rm.open_resource('TCPIP::192.168.0.1::INSTR') 
        # IP address above need to be set manually
        self.setup() # First calls for setup for measuring power

    def setup(self):
        # Measures power of a signal input to network analyzer
        print(self.inst)
        print(self.inst.write("*IDN?"))
        print (self.inst.read())
        self.inst.write("INST:SEL 'SA';*OPC?")
        self.inst.read()
        # If debug is true then user setting of start frequency, 
        # stop frequency and number of points
        if self.debug:
            self.inst.write("SENS:SWE:POIN " + str(self.numPoints))
            self.inst.write("SENS:FREQ:CENT " + str(self.centFreq))
            self.inst.write("SENS:FREQ:SPAN " + str(self.spanFreq))
            self.inst.write("SENS:BAND:RES 20")
            self.inst.write("DISP:WIND:TRAC1:Y:PDIV 15")
        self.inst.write("SENS:SWE:POIN?")
        self.numPoints = self.inst.read()
        print("Number of trace points " + self.numPoints)

    def VNAsetup(self):
        # Measures phase of the S11, S12, S21, S22 signal returns
        print(self.inst)
        print(self.inst.write("*IDN?"))
        print (self.inst.read())
        # Setup for NA mode
        self.inst.write("INST:SEL 'NA';*OPC?")
        self.inst.read()
        # Setup 2 channel S-parameters with a center frequency
        self.inst.write(":DISP:WIND:SPL D12_34")
        self.inst.write("FREQ:STAR 950e6")
        self.inst.write("FREQ:STOP 1050e6")
        self.inst.write("CORR 1")
        # Select S11, set it for phase measurement, and auto display
        self.inst.write("CALC:PAR1:SEL")
        self.inst.write("CALC:FORMat PHASe")
        self.inst.write("DISPlay:WINDow:TRAC1:Y:AUTO")
        # Select S21, set it for phase measurement, and auto display
        self.inst.write("CALC:PAR2:SEL")
        self.inst.write("CALC:FORMat PHASe")
        self.inst.write("DISPlay:WINDow:TRAC2:Y:AUTO")
        # Select S12, set it for phase measurement, and auto display
        self.inst.write("CALC:PAR3:SEL")
        self.inst.write("CALC:FORMat PHASe")
        self.inst.write("DISPlay:WINDow:TRAC3:Y:AUTO")
        # Select S22, set it for phase measurement, and auto display
        self.inst.write("CALC:PAR4:SEL")
        self.inst.write("CALC:FORMat PHASe")
        self.inst.write("DISPlay:WINDow:TRAC4:Y:AUTO")
        
    def save_s2p_file(self, name):
        # Saving s-parameters from scope's current display to s2p files
        # S2p files can be processed via matlab
        file_name = "\"" + str(name) + ".s2p"+ "\""
        self.inst.write("MMEM:STOR:SNP " + file_name)
        print("Save completed as: " + str(name))

    def get_maximum_power(self):    
        # Get maximum value of marker as a float
        self.inst.write("CALC:MARK1:FUNC:MAX")
        self.inst.write("CALC:MARK1:Y?")
        max_str = self.inst.read()
        max_str = float(max_str)
        # Get data on Trace 1 (string) and 
        # split them in an array of floats
        a = self.inst.write("TRAC1:DATA?")
        a_trace_data = self.inst.read()
        a_data_array = a_trace_data.split(",")
        npyarray = np.array(a_data_array)
        test = npyarray.astype(float)
        # Get max from the float array
        self.max_power = max(test) 
        return self.max_power
    
    def get_data(self):
        # Return data of Trace 1 in an array of x-values, and y-valus
        a = self.inst.write("TRAC1:DATA?")
        a_trace_data = self.inst.read()
        a_data_array = a_trace_data.split(",")
        npyarray = np.array(a_data_array)
        data = npyarray.astype(float)
        # Comments here help plot the data from the power measurements
        # retrieved from the scope 
        # plt.title("Keysight FieldFox Spectrum Trace Data via Python" +
        # " - PyVisa - SCPI")
        # plt.xlabel("Frequency")
        # plt.ylabel("Amplitude (dBm)")
        stimulusArray = np.linspace(float(self.centFreq - self.spanFreq/2),
                                    float(self.centFreq + self.spanFreq/2),
                                    int(self.numPoints))
        # print (stimulusArray)
        # plt.plot(stimulusArray, data)
        # plt.autoscale(True, True, True)
        # plt.show()
        return [stimulusArray, data]

# comments here help test scope functions above when needed
# scope = FieldFoxScope()
# scope.save_s2p_file("testSCB")
# s = scope.get_maximum_power()
# print(s)