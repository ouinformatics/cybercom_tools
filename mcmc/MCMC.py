import core.modules.module_registry
import os
from core.system import list2cmdline
from core.modules.vistrails_module import Module, ModuleError
version = "0.0.1"
name = "MCMC"
identifier = "edu.ou.it.vistrails.MCMC"
#class MCMCDataLoader(Module):
#	"""MCMC module for importing data from store to modle."""
#	def compute(self):
class MCMCModel(Module):
	"""Runs the MCMC Model"""
	def compute(self):
		run_type = self.getInputFromPort("RunType")
		run_count = self.getInputFromPort("Count")
		output_file = self.interpreter.filePool.create_file()
#		test_string = '/Users/blc/my_git/cybercom/mcmc/test_this'
#		os.system('cd /Users/blc/my_git/cybercom/mcmc;/usr/bin/matlab -nodisplay -r "MCMC 3 '+run_count +' '+ output_file.name+' "')
		copyline=['cd','/Users/blc/my_git/cybercom/mcmc',';','/usr/bin/matlab','-nodisplay','-r','MCMC '+run_type+' '+run_count+' '+output_file.name]
#		copyline=['cd','/Users/blc/my_git/cybercom/mcmc',';','/usr/bin/matlab','-nodisplay','-r','MCMC '+run_type+' '+run_count+' '+test_string]
		cline=list2cmdline(copyline)
		os.system(cline)
#		print cline
#		copyline=['/bin/cp',output_file.name,'/Users/blc/my_git/mcmc/test.inter']
#		cline=list2cmdline(copyline)
#		os.system(cline)
		self.setResult("Output_File", output_file)

class MCMCOut(Module):
	"""Handle matlab output file"""
	def compute(self):
		M_file=self.getInputFromPort("Model_Out")
		Output_File=self.getInputFromPort("Output_File")
		print(M_file.name)
		copyline=['/bin/cp', M_file.name+'.mat', Output_File]
		cline=list2cmdline(copyline)
		os.system(cline)

def initialize(*args, **keywords):
	reg=core.modules.module_registry.registry

	reg.add_module(MCMCModel)
	reg.add_input_port(MCMCModel, 'Count',
		(core.modules.basic_modules.String, 'Number of Iterations'))
	reg.add_input_port(MCMCModel, "RunType",
		(core.modules.basic_modules.String, '2 for ambient inversion, 3 for elevated inversion'))
	reg.add_output_port(MCMCModel, 'Output_File',
		(core.modules.basic_modules.File, 'Path and file for output'))

	reg.add_module(MCMCOut)
	reg.add_input_port(MCMCOut, 'Model_Out',
		(core.modules.basic_modules.File, 'File From Model'))
	reg.add_input_port(MCMCOut, 'Output_File',
		(core.modules.basic_modules.String, 'File and path to save from model'))
