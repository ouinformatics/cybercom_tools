import core.modules.module_registry
import os
import time
from subprocess import Popen
from subprocess import PIPE
from core.system import list2cmdline
from core.modules.vistrails_module import Module, ModuleError
version = "0.0.1"
name = "TECO"
identifier = "edu.ou.it.vistrails.TECO"
mpwd = "/home/bcremeans/my_git/cybercom/teco"
muhome = "/home/bcremeans/.oracle"
class TecoParameters(Module):
    "This should load and make seen the TECO parameters"""
    def compute(self):
        headers=["years_of_data","years_before_write","slat","co2ca","ioput","a1","Ds0","Vcmx0","extkU","xfang","alpha","stom_n","wsmax","wsmin","rdepth","rfibre","SLA","LAIMAX","LAIMIN"]

        tp_years_of_data=self.getInputFromPort("years_of_data")
        tp_years_before_write=self.getInputFromPort("years_before_write")
        tp_slat=self.getInputFromPort("slat")
        tp_co2ca=self.getInputFromPort("co2ca")
        tp_ioput=self.getInputFromPort("ioput")
        tp_a1=self.getInputFromPort("a1")
        tp_Ds0=self.getInputFromPort("Ds0")
        tp_Vcmx0=self.getInputFromPort("Vcmx0")
        tp_extkU=self.getInputFromPort("extkU")
        tp_xfang=self.getInputFromPort("xfang")
        tp_alpha=self.getInputFromPort("alpha")
        tp_stom_n=self.getInputFromPort("stom_n")
        tp_wsmax=self.getInputFromPort("wsmax")
        tp_wsmin=self.getInputFromPort("wsmin")
        tp_rdepth=self.getInputFromPort("rdepth")
        tp_rfibre=self.getInputFromPort("rfibre")
        tp_SLA=self.getInputFromPort("SLA")
        tp_LAIMAX=self.getInputFromPort("LAIMAX")
        tp_LAIMIN=self.getInputFromPort("LAIMIN")

        param_vals=[tp_years_of_data,tp_years_before_write,tp_slat,tp_co2ca,tp_ioput,tp_a1,tp_Ds0,tp_Vcmx0,tp_extkU,tp_xfang,tp_alpha,tp_stom_n,tp_wsmax,tp_wsmin,tp_rdepth,tp_rfibre,tp_SLA,tp_LAIMAX,tp_LAIMIN]

        self.setResult("years_of_data", tp_years_of_data)
        self.setResult("years_before_write", tp_years_before_write)
        self.setResult("slat", tp_slat)
        self.setResult("co2ca", tp_co2ca)
        self.setResult("ioput", tp_ioput)
        self.setResult("a1", tp_a1)
        self.setResult("Ds0", tp_Ds0)
        self.setResult("Vcmx0", tp_Vcmx0)
        self.setResult("extkU", tp_extkU)
        self.setResult("xfang", tp_xfang)
        self.setResult("alpha", tp_alpha)
        self.setResult("stom_n", tp_stom_n)
        self.setResult("wsmax", tp_wsmax)
        self.setResult("wsmin", tp_wsmin)
        self.setResult("rdepth", tp_rdepth)
        self.setResult("rfibre", tp_rfibre)
        self.setResult("SLA", tp_SLA)
        self.setResult("LAIMAX", tp_LAIMAX)
        self.setResult("LAIMIN", tp_LAIMIN)
        self.setResult("headers",headers)
        self.setResult("param_vals",param_vals)

class TecoDataLoader(Module):
    """TecoDataLoader is a data importing module for the TECO carbon model"""
    def compute(self):
        ifp = self.getInputFromPort("InputDataFilePath")
        Data_File=self.interpreter.filePool.create_file()
        cline=['cp',ifp,Data_File.name]
        Popen(cline)
        #os.system('cat '+ ifp + '>' +Data_File.name)
        self.setResult("DataFilePath", Data_File)

class TecoDBLoader(Module):
    """TecoDBLoader is a data importing module for the TECO carbon model"""
    def compute(self):
        ifp = self.getInputFromPort("RunID")
        Data_File=self.interpreter.filePool.create_file()
        cline=[mpwd+'/INP_2_TECO.py',ifp,'TECO1',Data_File.name]
        Popen(cline,env={'LD_LIBRARY_PATH':'/usr/local/oracle/instantclient_10_2','TNS_ADMIN':muhome,'PYTHONPATH':'PYTHONPATH=/usr/lib/python2.6/site-packages'}).wait()
        self.setResult("DataFilePath", Data_File)

class TecoRunID(Module):
    def compute(self):
        run_name=self.getInputFromPort("RunName")
        run_desc=self.getInputFromPort("RunDesc")
        cline=[mpwd+'/get_run_id.py',run_name,run_desc, 'TECO1']
        cri = Popen(cline,env={'LD_LIBRARY_PATH':'/usr/local/oracle/instantclient_10_2','TNS_ADMIN':muhome,'PYTHONPATH':'PYTHONPATH=/usr/lib/python2.6/site-packages'},stdout=PIPE)
        time.sleep(5)
        run_id = cri.communicate()[0].strip()
        print run_id
        self.setResult("RUN_ID", run_id)

class TecoINP2DB(Module):
    def compute(self):
        RUN_ID=self.getInputFromPort("RUN_ID")
        file_name=self.getInputFromPort("file_name")
        cline=[mpwd+'/file_to_db.py',RUN_ID,file_name.name]
        cri = Popen(cline,env={'LD_LIBRARY_PATH':'/usr/local/oracle/instantclient_10_2','TNS_ADMIN':muhome,'PYTHONPATH':'PYTHONPATH=/usr/lib/python2.6/site-packages'},stdout=PIPE)

class TecoModel(Module):
    """"TecoModel runs the TECO Carbon Model"""
    def compute(self):
        data_file=self.getInputFromPort("InputDataFile")
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
        cargs=[mpwd+'/teco_cli_parm' ,years_of_data, years_before_write, data_file.name, C_file.name, H2O_file.name, Pools_file.name, slat, co2ca, ioput, a1, Ds0, Vcmx0, extkU, xfang, alpha, stom_n, wsmax, wsmin, rdepth, rfibre, SLA, LAIMAX, LAIMIN]
        #cline=list2cmdline(cargs)
        #os.system(cline)
        Popen(cargs)
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
        #cline=list2cmdline(copyline)
        #os.system(cline)
        Popen(copyline)
        copyline=['/bin/cp', H2O_file.name, H2O_Write]
        #cline=list2cmdline(copyline)
        #os.system(cline)
        Popen(copyline)
        copyline=['/bin/cp', Pools_file.name, Pools_Write]
        #cline=list2cmdline(copyline)
        #os.system(cline)
        Popen(copyline)
        self.setResult("C_Out",C_file);
        self.setResult("H2O_Out",H2O_file);
        self.setResult("Pools_Out",Pools_file);

class TecoDBOutput(Module):
    def compute(self):
        RUN_ID=self.getInputFromPort("RUN_ID")
        C_Write=self.getInputFromPort("C_Out")
        H2O_Write=self.getInputFromPort("H2O_Out")
        Pools_Write=self.getInputFromPort("Pools_Out")
        cline=[mpwd+'/test.py',RUN_ID,C_Write.name,H2O_Write.name,Pools_Write.name]
        Popen(cline,env={'LD_LIBRARY_PATH':'/usr/local/oracle/instantclient_10_2','TNS_ADMIN':muhome,'PYTHONPATH':'PYTHONPATH=/usr/lib/python2.6/site-packages'}).wait()
        
###############################################################################
def initialize(*args, **keywords):
    reg = core.modules.module_registry.registry
    reg.add_module(TecoParameters)
    reg.add_input_port(TecoParameters, 'years_of_data', (core.modules.basic_modules.String, 'Number of years covered by the Amb data'),defaults=str(['1']))
    reg.add_input_port(TecoParameters, 'years_before_write', (core.modules.basic_modules.String, 'Number of years ran before writing data'),defaults=str(['3']))
    reg.add_input_port(TecoParameters, 'slat', (core.modules.basic_modules.String, 'slat'),defaults=str(['35.9']))
    reg.add_input_port(TecoParameters, 'co2ca', (core.modules.basic_modules.String, 'co2ca'),defaults=str(['3.70E-04']))
    reg.add_input_port(TecoParameters, 'ioput', (core.modules.basic_modules.String, 'ioput'),defaults=str(['2']))
    reg.add_input_port(TecoParameters, 'a1', (core.modules.basic_modules.String, 'a1'),defaults=str(['7.0']))
    reg.add_input_port(TecoParameters, 'Ds0', (core.modules.basic_modules.String, 'Ds0'),defaults=str(['2000']))
    reg.add_input_port(TecoParameters, 'Vcmx0', (core.modules.basic_modules.String, 'Vcmx0'),defaults=str(['0.80E-04']))
    reg.add_input_port(TecoParameters, 'extkU', (core.modules.basic_modules.String, 'extkU'),defaults=str(['0.5']))
    reg.add_input_port(TecoParameters, 'xfang', (core.modules.basic_modules.String, 'xfang'),defaults=str(['0']))
    reg.add_input_port(TecoParameters, 'alpha', (core.modules.basic_modules.String, 'alpha'),defaults=str(['0.385']))
    reg.add_input_port(TecoParameters, 'stom_n', (core.modules.basic_modules.String, 'stom_n'),defaults=str(['2']))
    reg.add_input_port(TecoParameters, 'wsmax', (core.modules.basic_modules.String, 'wsmax'),defaults=str(['35']))
    reg.add_input_port(TecoParameters, 'wsmin', (core.modules.basic_modules.String, 'wsmin'),defaults=str(['6']))
    reg.add_input_port(TecoParameters, 'rdepth', (core.modules.basic_modules.String, 'rdepth'),defaults=str(['70.0']))
    reg.add_input_port(TecoParameters, 'rfibre', (core.modules.basic_modules.String, 'rfibre'),defaults=str(['0.7']))
    reg.add_input_port(TecoParameters, 'SLA', (core.modules.basic_modules.String, 'SLA'),defaults=str(['1.2E-02']))
    reg.add_input_port(TecoParameters, 'LAIMAX', (core.modules.basic_modules.String, 'LAIMAX'),defaults=str(['4.5']))
    reg.add_input_port(TecoParameters, 'LAIMIN', (core.modules.basic_modules.String, 'LAIMIN'),defaults=str(['0.1']))

    reg.add_output_port(TecoParameters, 'param_vals', (core.modules.basic_modules.List, 'param_vals'))
    reg.add_output_port(TecoParameters, 'headers', (core.modules.basic_modules.List, 'headers'))
    reg.add_output_port(TecoParameters, 'LAIMIN', (core.modules.basic_modules.String, 'LAIMIN'))
    reg.add_output_port(TecoParameters, 'LAIMAX', (core.modules.basic_modules.String, 'LAIMAX'))
    reg.add_output_port(TecoParameters, 'SLA', (core.modules.basic_modules.String, 'SLA'))
    reg.add_output_port(TecoParameters, 'rfibre', (core.modules.basic_modules.String, 'rfibre'))
    reg.add_output_port(TecoParameters, 'rdepth', (core.modules.basic_modules.String, 'rdepth'))
    reg.add_output_port(TecoParameters, 'wsmin', (core.modules.basic_modules.String, 'wsmin'))
    reg.add_output_port(TecoParameters, 'wsmax', (core.modules.basic_modules.String, 'wsmax'))
    reg.add_output_port(TecoParameters, 'stom_n', (core.modules.basic_modules.String, 'stom_n'))
    reg.add_output_port(TecoParameters, 'alpha', (core.modules.basic_modules.String, 'alpha'))
    reg.add_output_port(TecoParameters, 'xfang', (core.modules.basic_modules.String, 'xfang'))
    reg.add_output_port(TecoParameters, 'extkU', (core.modules.basic_modules.String, 'extkU'))
    reg.add_output_port(TecoParameters, 'Vcmx0', (core.modules.basic_modules.String, 'Vcmx0'))
    reg.add_output_port(TecoParameters, 'Ds0', (core.modules.basic_modules.String, 'Ds0'))
    reg.add_output_port(TecoParameters, 'a1', (core.modules.basic_modules.String, 'a1'))
    reg.add_output_port(TecoParameters, 'ioput', (core.modules.basic_modules.String, 'ioput'))
    reg.add_output_port(TecoParameters, 'co2ca', (core.modules.basic_modules.String, 'co2ca'))
    reg.add_output_port(TecoParameters, 'slat', (core.modules.basic_modules.String, 'slat'))
    reg.add_output_port(TecoParameters, 'years_before_write', (core.modules.basic_modules.String, 'Number of years ran before writing data'))
    reg.add_output_port(TecoParameters, 'years_of_data', (core.modules.basic_modules.String, 'Number of years covered by the Amb data'))

    reg.add_module(TecoDataLoader)
    reg.add_input_port(TecoDataLoader, 'InputDataFilePath',
                      (core.modules.basic_modules.String, 'Path and Filename for datafile'))
    reg.add_output_port(TecoDataLoader, "DataFilePath",
                       (core.modules.basic_modules.File, 'Path and Filename for datafile to model'))

    reg.add_module(TecoDBLoader)
    reg.add_input_port(TecoDBLoader, 'RunID',
                      (core.modules.basic_modules.String, 'RunID'),defaults=str(['500']))
    reg.add_output_port(TecoDBLoader, "DataFilePath",
                       (core.modules.basic_modules.File, 'Path and Filename for datafile to model'))
    reg.add_output_port(TecoDBLoader, "RunID",
                       (core.modules.basic_modules.String, 'RunID'))

    reg.add_module(TecoModel)
    reg.add_input_port(TecoModel, 'InputDataFile',
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

    reg.add_output_port(TecoModel, 'Pools_File',
                      (core.modules.basic_modules.File, 'Path to Pools Output File'))
    reg.add_output_port(TecoModel, 'H2O_File',
                      (core.modules.basic_modules.File, 'Path to H2O Output File'))
    reg.add_output_port(TecoModel, 'C_File',
                      (core.modules.basic_modules.File, 'Path to C Output File'))

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

    reg.add_output_port(TecoOutput, 'Pools_Out',
                      (core.modules.basic_modules.File, 'Path to Pools File'))
    reg.add_output_port(TecoOutput, 'H2O_Out',
                      (core.modules.basic_modules.File, 'Path to H2O File'))
    reg.add_output_port(TecoOutput, 'C_Out',
                      (core.modules.basic_modules.File, 'Path to Cs File'))

    reg.add_module(TecoDBOutput)
    
    reg.add_input_port(TecoDBOutput, 'RUN_ID',
                      (core.modules.basic_modules.String, 'RUN_ID'))
    reg.add_input_port(TecoDBOutput, 'C_Out',
                      (core.modules.basic_modules.File, 'C File from model'))
    reg.add_input_port(TecoDBOutput, 'H2O_Out',
                      (core.modules.basic_modules.File, 'H2O File from model'))
    reg.add_input_port(TecoDBOutput, 'Pools_Out',
                      (core.modules.basic_modules.File, 'C File from model'))

    reg.add_module(TecoRunID)

    reg.add_output_port(TecoRunID, 'RUN_ID',
                       (core.modules.basic_modules.String, 'RUN_ID'))
    reg.add_input_port(TecoRunID, 'RunName',
                       (core.modules.basic_modules.String, 'RunName'),defaults=str(['Teco_Default']))
    reg.add_input_port(TecoRunID, 'RunDesc',
                       (core.modules.basic_modules.String, 'RunDesc'),defaults=str(['Teco_Run']))

    reg.add_module(TecoINP2DB)

    reg.add_input_port(TecoINP2DB, 'RUN_ID', (core.modules.basic_modules.String, 'RUN_ID'))
    reg.add_input_port(TecoINP2DB, 'file_name', (core.modules.basic_modules.File, 'file_name'))
