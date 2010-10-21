import core.modules.module_registry
import os
from core.system import list2cmdline
from core.modules.vistrails_module import Module, ModuleError
version = "0.0.1"
name = "TECO"
identifier = "edu.ou.it.vistrails.TECO"
class TecoDataLoader(Module):
    """TecoDataLoader is a data importing module for the TECO carbon model"""
    def compute(self):
        ifp = self.getInputFromPort("InputDataFilePath")
        pfp = self.getInputFromPort("InputParamFilePath")
        Data_File=self.interpreter.filePool.create_file()
        Param_File=self.interpreter.filePool.create_file()
        os.system('cat '+ ifp + '>' +Data_File.name)
        os.system('cat '+ pfp + '>' +Param_File.name)
        self.setResult("DataFilePath", Data_File)
        self.setResult("ParameterFilePath", Param_File)
class TecoModel(Module):
    """"TecoModel runs the TECO Carbon Model"""
    def compute(self):
        data_file=self.getInputFromPort("InputDataFile")
        param_file=self.getInputFromPort("InputParameterFile")
#        C_file=self.getInputFromPort("C_File")
#        H2O_file=self.getInputFromPort("H2O_File")
#        Pools_file=self.getInputFromPort("Pools_File")
        C_file=self.interpreter.filePool.create_file()
        H2O_file=self.interpreter.filePool.create_file()
        Pools_file=self.interpreter.filePool.create_file()
        cargs=['/Users/blc/my_git/cybercom/teco/teconew' ,param_file.name, data_file.name, C_file.name, H2O_file.name, Pools_file.name]
        cline=list2cmdline(cargs)
        os.system(cline)
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
        os.system(cline)
        copyline=['/bin/cp', H2O_file.name, H2O_Write]
        cline=list2cmdline(copyline)
        os.system(cline)
        copyline=['/bin/cp', Pools_file.name, Pools_Write]
        cline=list2cmdline(copyline)
        os.system(cline)
###############################################################################
def initialize(*args, **keywords):
    reg = core.modules.module_registry.registry
    reg.add_module(TecoDataLoader)
    reg.add_input_port(TecoDataLoader, 'InputDataFilePath',
                      (core.modules.basic_modules.String, 'Path and Filename for datafile'))
    reg.add_input_port(TecoDataLoader, 'InputParamFilePath',
                      (core.modules.basic_modules.String, 'Path and Filename for paramaeter file'))
    reg.add_output_port(TecoDataLoader, "DataFilePath",
                       (core.modules.basic_modules.File, 'Path and Filename for datafile to model'))
    reg.add_output_port(TecoDataLoader, "ParameterFilePath",
                       (core.modules.basic_modules.File, 'Path and Filename for parameter to model'))
    reg.add_module(TecoModel)
    reg.add_input_port(TecoModel, 'InputParameterFile',
                      (core.modules.basic_modules.File, 'Path to Parameter File'))
    reg.add_input_port(TecoModel, 'InputDataFile',
                      (core.modules.basic_modules.File, 'Path to Data File'))
    reg.add_input_port(TecoModel, 'C_File',
                      (core.modules.basic_modules.File, 'Path to Data File'))
    reg.add_input_port(TecoModel, 'H2O_File',
                      (core.modules.basic_modules.File, 'Path to Data File'))
    reg.add_input_port(TecoModel, 'Pools_File',
                      (core.modules.basic_modules.File, 'Path to Data File'))
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
