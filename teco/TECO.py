import core.modules.module_registry
import os
from subprocess import Popen
from core.system import list2cmdline
from core.modules.vistrails_module import Module, ModuleError
version = "0.0.1"
name = "TECO"
identifier = "edu.ou.it.vistrails.TECO"
class TecoParameters(Module):
    "This should load and make seen the TECO parameters"""
    def compute(self):
        self.setResult("years_of_data", self.getInputFromPort("years_of_data"))
        self.setResult("years_before_write", self.getInputFromPort("years_before_write"))
        self.setResult("slat", self.getInputFromPort("slat"))
        self.setResult("co2ca", self.getInputFromPort("co2ca"))
        self.setResult("ioput", self.getInputFromPort("ioput"))
        self.setResult("a1", self.getInputFromPort("a1"))
        self.setResult("Ds0", self.getInputFromPort("Ds0"))
        self.setResult("Vcmx0", self.getInputFromPort("Vcmx0"))
        self.setResult("extkU", self.getInputFromPort("extkU"))
        self.setResult("xfang", self.getInputFromPort("xfang"))
        self.setResult("alpha", self.getInputFromPort("alpha"))
        self.setResult("stom_n", self.getInputFromPort("stom_n"))
        self.setResult("wsmax", self.getInputFromPort("wsmax"))
        self.setResult("wsmin", self.getInputFromPort("wsmin"))
        self.setResult("rdepth", self.getInputFromPort("rdepth"))
        self.setResult("rfibre", self.getInputFromPort("rfibre"))
        self.setResult("SLA", self.getInputFromPort("SLA"))
        self.setResult("LAIMAX", self.getInputFromPort("LAIMAX"))
        self.setResult("LAIMIN", self.getInputFromPort("LAIMIN"))
class TecoDataLoader(Module):
    """TecoDataLoader is a data importing module for the TECO carbon model"""
    def compute(self):
        ifp = self.getInputFromPort("InputDataFilePath")
#        pfp = self.getInputFromPort("InputParamFilePath")
        Data_File=self.interpreter.filePool.create_file()
#        Param_File=self.interpreter.filePool.create_file()
        os.system('cat '+ ifp + '>' +Data_File.name)
#        os.system('cat '+ pfp + '>' +Param_File.name)
        self.setResult("DataFilePath", Data_File)
#        self.setResult("ParameterFilePath", Param_File)

class TecoModel(Module):
    """"TecoModel runs the TECO Carbon Model"""
    def compute(self):
        data_file=self.getInputFromPort("InputDataFile")
#        param_file=self.getInputFromPort("InputParameterFile")
        years_of_data=self.getInputFromPort("years_of_data")
        years_before_write=self.getInputFromPort("years_before_write")
        slat=self.getInputFromPort("slat")
        co2ca=self.getInputFromPort("co2ca")
        ioput=self.getInputFromPort("ioput")
        a1=self.getInputFromPort("a1")
        Ds0=self.getInputFromPort("Ds0")
        Vcmx0=self.getInputFromPort("Vcmx0")
        extkU=self.getInputFromPort("extkU")
        xfang=self.getInputFromPort("xfang")
        alpha=self.getInputFromPort("alpha")
        stom_n=self.getInputFromPort("stom_n")
        wsmax=self.getInputFromPort("wsmax")
        wsmin=self.getInputFromPort("wsmin")
        rdepth=self.getInputFromPort("rdepth")
        rfibre=self.getInputFromPort("rfibre")
        SLA=self.getInputFromPort("SLA")
        LAIMAX=self.getInputFromPort("LAIMAX")
        LAIMIN=self.getInputFromPort("LAIMIN")
        C_file=self.interpreter.filePool.create_file()
        H2O_file=self.interpreter.filePool.create_file()
        Pools_file=self.interpreter.filePool.create_file()
        cargs=['/Users/blc/my_git/cybercom/teco/teco_cli_param' ,years_of_data, years_before_write, data_file.name, C_file.name, H2O_file.name, Pools_file.name, slat, co2ca, ioput, a1, Ds0, Vcmx0, extkU, xfang, alpha, stom_n, wsmax, wsmin, rdepth, rfibre, SLA, LAIMAX, LAIMIN]
        cline=list2cmdline(cargs)
        print cline
        os.system(cline)
#        Popen(cargs)
        self.setResult("C_File",C_file);
        self.setResult("H2O_File",H2O_file);
        self.setResult("Pools_File",Pools_file);

class TecoOutput(Module):
    def compute(self):
        C_file=self.getInputFromPort("C_Out")
        H2O_file=self.getInputFromPort("H2O_Out")
        Pools_file=self.getInputFromPort("Pools_Out")
        C_Write=self.getInputFromPort("C_File")
        H2O_Write=self.getInputFromPort("H2O_File")
        Pools_Write=self.getInputFromPort("Pools_File")
        copyline=['/bin/cp', C_file.name, C_Write]
        cline=list2cmdline(copyline)
#        Popen(copyline)
        os.system(cline)
        copyline=['/bin/cp', H2O_file.name, H2O_Write]
        cline=list2cmdline(copyline)
#        Popen(copyline)
        os.system(cline)
        copyline=['/bin/cp', Pools_file.name, Pools_Write]
        cline=list2cmdline(copyline)
#        Popen(copyline)
        os.system(cline)
        self.setResult("C_Out",C_file);
        self.setResult("H2O_Out",H2O_file);
        self.setResult("Pools_Out",Pools_file);
###############################################################################
def initialize(*args, **keywords):
    reg = core.modules.module_registry.registry
    reg.add_module(TecoParameters)
    reg.add_input_port(TecoParameters, 'years_of_data', (core.modules.basic_modules.String, 'Number of years covered by the Amb data'))
    reg.add_input_port(TecoParameters, 'years_before_write', (core.modules.basic_modules.String, 'Number of years ran before writing data'))
    reg.add_input_port(TecoParameters, 'slat', (core.modules.basic_modules.String, 'slat'))
    reg.add_input_port(TecoParameters, 'co2ca', (core.modules.basic_modules.String, 'co2ca'))
    reg.add_input_port(TecoParameters, 'ioput', (core.modules.basic_modules.String, 'ioput'))
    reg.add_input_port(TecoParameters, 'a1', (core.modules.basic_modules.String, 'a1'))
    reg.add_input_port(TecoParameters, 'Ds0', (core.modules.basic_modules.String, 'Ds0'))
    reg.add_input_port(TecoParameters, 'Vcmx0', (core.modules.basic_modules.String, 'Vcmx0'))
    reg.add_input_port(TecoParameters, 'extkU', (core.modules.basic_modules.String, 'extkU'))
    reg.add_input_port(TecoParameters, 'xfang', (core.modules.basic_modules.String, 'xfang'))
    reg.add_input_port(TecoParameters, 'alpha', (core.modules.basic_modules.String, 'alpha'))
    reg.add_input_port(TecoParameters, 'stom_n', (core.modules.basic_modules.String, 'stom_n'))
    reg.add_input_port(TecoParameters, 'wsmax', (core.modules.basic_modules.String, 'wsmax'))
    reg.add_input_port(TecoParameters, 'wsmin', (core.modules.basic_modules.String, 'wsmin'))
    reg.add_input_port(TecoParameters, 'rdepth', (core.modules.basic_modules.String, 'rdepth'))
    reg.add_input_port(TecoParameters, 'rfibre', (core.modules.basic_modules.String, 'rfibre'))
    reg.add_input_port(TecoParameters, 'SLA', (core.modules.basic_modules.String, 'SLA'))
    reg.add_input_port(TecoParameters, 'LAIMAX', (core.modules.basic_modules.String, 'LAIMAX'))
    reg.add_input_port(TecoParameters, 'LAIMIN', (core.modules.basic_modules.String, 'LAIMIN'))

    reg.add_output_port(TecoParameters, 'years_of_data', (core.modules.basic_modules.String, 'Number of years covered by the Amb data'))
    reg.add_output_port(TecoParameters, 'years_before_write', (core.modules.basic_modules.String, 'Number of years ran before writing data'))
    reg.add_output_port(TecoParameters, 'slat', (core.modules.basic_modules.String, 'slat'))
    reg.add_output_port(TecoParameters, 'co2ca', (core.modules.basic_modules.String, 'co2ca'))
    reg.add_output_port(TecoParameters, 'ioput', (core.modules.basic_modules.String, 'ioput'))
    reg.add_output_port(TecoParameters, 'a1', (core.modules.basic_modules.String, 'a1'))
    reg.add_output_port(TecoParameters, 'Ds0', (core.modules.basic_modules.String, 'Ds0'))
    reg.add_output_port(TecoParameters, 'Vcmx0', (core.modules.basic_modules.String, 'Vcmx0'))
    reg.add_output_port(TecoParameters, 'extkU', (core.modules.basic_modules.String, 'extkU'))
    reg.add_output_port(TecoParameters, 'xfang', (core.modules.basic_modules.String, 'xfang'))
    reg.add_output_port(TecoParameters, 'alpha', (core.modules.basic_modules.String, 'alpha'))
    reg.add_output_port(TecoParameters, 'stom_n', (core.modules.basic_modules.String, 'stom_n'))
    reg.add_output_port(TecoParameters, 'wsmax', (core.modules.basic_modules.String, 'wsmax'))
    reg.add_output_port(TecoParameters, 'wsmin', (core.modules.basic_modules.String, 'wsmin'))
    reg.add_output_port(TecoParameters, 'rdepth', (core.modules.basic_modules.String, 'rdepth'))
    reg.add_output_port(TecoParameters, 'rfibre', (core.modules.basic_modules.String, 'rfibre'))
    reg.add_output_port(TecoParameters, 'SLA', (core.modules.basic_modules.String, 'SLA'))
    reg.add_output_port(TecoParameters, 'LAIMAX', (core.modules.basic_modules.String, 'LAIMAX'))
    reg.add_output_port(TecoParameters, 'LAIMIN', (core.modules.basic_modules.String, 'LAIMIN'))

    reg.add_module(TecoDataLoader)
    reg.add_input_port(TecoDataLoader, 'InputDataFilePath',
                      (core.modules.basic_modules.String, 'Path and Filename for datafile'))
#    reg.add_input_port(TecoDataLoader, 'InputParamFilePath',
#                      (core.modules.basic_modules.String, 'Path and Filename for paramaeter file'))
    reg.add_output_port(TecoDataLoader, "DataFilePath",
                       (core.modules.basic_modules.File, 'Path and Filename for datafile to model'))
#    reg.add_output_port(TecoDataLoader, "ParameterFilePath",
#                       (core.modules.basic_modules.File, 'Path and Filename for parameter to model'))

    reg.add_module(TecoModel)
#    reg.add_input_port(TecoModel, 'InputParameterFile',
#                      (core.modules.basic_modules.File, 'Path to Parameter File'))
    reg.add_input_port(TecoModel, 'InputDataFile',
                      (core.modules.basic_modules.File, 'Path to Data File'))
    reg.add_input_port(TecoModel, 'C_File',
                      (core.modules.basic_modules.File, 'Path to Data File'))
    reg.add_input_port(TecoModel, 'H2O_File',
                      (core.modules.basic_modules.File, 'Path to Data File'))
    reg.add_input_port(TecoModel, 'Pools_File',
                      (core.modules.basic_modules.File, 'Path to Data File'))
    reg.add_input_port(TecoModel, 'years_of_data', (core.modules.basic_modules.String, 'Number of years covered by the Amb data'))
    reg.add_input_port(TecoModel, 'years_before_write', (core.modules.basic_modules.String, 'Number of years ran before writing data'))
    reg.add_input_port(TecoModel, 'slat', (core.modules.basic_modules.String, 'slat'))
    reg.add_input_port(TecoModel, 'co2ca', (core.modules.basic_modules.String, 'co2ca'))
    reg.add_input_port(TecoModel, 'ioput', (core.modules.basic_modules.String, 'ioput'))
    reg.add_input_port(TecoModel, 'a1', (core.modules.basic_modules.String, 'a1'))
    reg.add_input_port(TecoModel, 'Ds0', (core.modules.basic_modules.String, 'Ds0'))
    reg.add_input_port(TecoModel, 'Vcmx0', (core.modules.basic_modules.String, 'Vcmx0'))
    reg.add_input_port(TecoModel, 'extkU', (core.modules.basic_modules.String, 'extkU'))
    reg.add_input_port(TecoModel, 'xfang', (core.modules.basic_modules.String, 'xfang'))
    reg.add_input_port(TecoModel, 'alpha', (core.modules.basic_modules.String, 'alpha'))
    reg.add_input_port(TecoModel, 'stom_n', (core.modules.basic_modules.String, 'stom_n'))
    reg.add_input_port(TecoModel, 'wsmax', (core.modules.basic_modules.String, 'wsmax'))
    reg.add_input_port(TecoModel, 'wsmin', (core.modules.basic_modules.String, 'wsmin'))
    reg.add_input_port(TecoModel, 'rdepth', (core.modules.basic_modules.String, 'rdepth'))
    reg.add_input_port(TecoModel, 'rfibre', (core.modules.basic_modules.String, 'rfibre'))
    reg.add_input_port(TecoModel, 'SLA', (core.modules.basic_modules.String, 'SLA'))
    reg.add_input_port(TecoModel, 'LAIMAX', (core.modules.basic_modules.String, 'LAIMAX'))
    reg.add_input_port(TecoModel, 'LAIMIN', (core.modules.basic_modules.String, 'LAIMIN'))

    reg.add_output_port(TecoModel, 'C_File',
                      (core.modules.basic_modules.File, 'Path to C Output File'))
    reg.add_output_port(TecoModel, 'H2O_File',
                      (core.modules.basic_modules.File, 'Path to H2O Output File'))
    reg.add_output_port(TecoModel, 'Pools_File',
                      (core.modules.basic_modules.File, 'Path to Pools Output File'))

    reg.add_module(TecoOutput)

    reg.add_input_port(TecoOutput, 'C_Out',
                      (core.modules.basic_modules.File, 'C File from model'))
    reg.add_input_port(TecoOutput, 'H2O_Out',
                      (core.modules.basic_modules.File, 'H2O File from model'))
    reg.add_input_port(TecoOutput, 'Pools_Out',
                      (core.modules.basic_modules.File, 'C File from model'))
    reg.add_input_port(TecoOutput, 'C_File',
                      (core.modules.basic_modules.String, 'Path to C File'))
    reg.add_input_port(TecoOutput, 'H2O_File',
                      (core.modules.basic_modules.String, 'Path to H2O File'))
    reg.add_input_port(TecoOutput, 'Pools_File',
                      (core.modules.basic_modules.String, 'Path to Pools File'))

    reg.add_output_port(TecoOutput, 'C_Out',
                      (core.modules.basic_modules.File, 'Path to Cs File'))
    reg.add_output_port(TecoOutput, 'H2O_Out',
                      (core.modules.basic_modules.File, 'Path to H2O File'))
    reg.add_output_port(TecoOutput, 'Pools_Out',
                      (core.modules.basic_modules.File, 'Path to Pools File'))
