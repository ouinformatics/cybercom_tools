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
#		cargs=['/usr/bin/matlab','-nodisplay','-r','MCMC'
		os.system('cd /Users/blc/carbon/mcmc;/usr/bin/matlab -nodisplay -r "MCMC 3 '+run_count +' '+ output_file.name+' "')
def initialize(*args, **keywords):
	reg=core.modules.module_registry.registry
	reg.add_module(MCMCModel)
	reg.add_input_port(MCMCModel, 'Count',
		(core.modules.basic_modules.String, 'Number of Iterations'))
	reg.add_input_port(MCMCModel, "RunType",
		(core.modules.basic_modules.String, '2 for ambient inversion, 3 for elevated inversion'))
	reg.add_output_port(MCMCModel, 'Output_File',
		(core.modules.basic_modules.File, 'Path and file for output'))
