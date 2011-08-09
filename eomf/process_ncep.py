#!/usr/bin/python2.6

from aggregate_ncep import aggregate_ncep
import os

variables = [ { 'variable': 'pr_wtr', 'method': 'sum', 'form': 'pr_wtr.eatm.YYYY.nc' },
              { 'variable': 'air', 'method': 'avg', 'form': 'air.sig995.YYYY.nc' },
              { 'variable': 'rhum', 'method':'avg', 'form': 'rhum.sig995.YYYY.nc' },
              { 'variable': 'pres', 'method': 'avg', 'form': 'pres.sfc.YYYY.nc'} ]

aggregates = ['daily','week','8day','month','annual']

def do_aggregation(years, variables):
    for year in years:
        for variable in variables:
            for aggregate in aggregates:
                print aggregate 
                fname = os.path.join(variable['variable'], variable['form'].replace('YYYY', str(year)))
                aggregate_ncep(fname, aggregate, variable['method'])

#do_aggregation(range(1980,2012), variables)
do_aggregation([2011], variables)
