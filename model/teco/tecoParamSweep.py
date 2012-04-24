from urllib2 import urlopen
import json,pickle
from pymongo import Connection

db=Connection('129.15.41.76').cybercom_queue
#siteparam
siteparam="{'Q_leaf':1,'rdepth':82.577,'GLmax':0.05874,'Tau_Passive':919.25,'nsc':85.35,'Q_micr':895,'site':'US-HA1','Gamma_Wmax':0.00015,'Stemmax':859.58,'S_w_min':0.5,'LAIMIN':1e-05,'Tau_Wood':12.239,'NEEfile':'HarvardForest_hr_Chuixiang.txt','ToptV':32.963,'outputfile':'US-Ha1','vegtype':'DBF','GRmax':0.08353,'LAIMAX':5.32,'Q_coarse':7760,'co2ca':3.70E-04,'SLA':0.05298,'Q_root3':0,'Q_root2':0,'Q_root1':120,'TminV':-6.3833,'extkU':0.5,'wsmax':20.907,'inputfile':'US-Ha1forcing.txt','SapR':0.31018,'SapS':0.1034,'Vcmx0':0.00015,'Q_wood':33800,'wsmin':5.5638,'stom_n':2,'Gsmax':0.12698,'Tau_Micro':0.58136,'Ds0':2565.8,'xfang':0,'a1':26.717,'Longitude':-72.1715,'TmaxV':47.934,'lat':42.5378,'alpha':0.17812,'Q10_h':2.2,'Tcold':10.733,'Tau_Leaf':0.85114,'Gamma_Tmax':0.00161,'Q_pass':3820,'Tau_F':2.0534,'Tau_C':3.3147,'Tau_Root':0.50489,'Q_slow':17200,'gddonset':584.38,'Tau_SlowSOM':15.633,'Q_fine':1980,'Rootmax':876.45,}"

cur_site = 'US-HA1'
base_yrs='(2006,2006)'
forc='[]'
MW_template="{'T_air':[('add',%d)]}"
output =[]
#Run Workflow
for tempinc in range(0,11):
    #adjust waether
    mod_weather=MW_template % (tempinc)
    #Set Params
    param= "site=" + cur_site + "&base_yrs=" + base_yrs + "&forecast=" + forc + "&siteparam=" + str(siteparam) + "&mod_weather=" + mod_weather
    url ="http://test.cybercommons.org/queue/run/cybercomq.model.teco.task.runTECOworkflow/?" + param
    #Run Workflow
    temp= json.loads(urlopen(url).read())
    #Add temp variation to output and report url
    temp['Temp_Added']=tempinc
    temp['Result_URL']="http://test.cybercommons.org/queue/report/" + temp['task_id']
    output.append(temp)
#Add tecoresult task_id for plotting
for row in output:
    tresult= db['cybercom_queue_meta'].find({'_id':row['task_id']})
    if not tresult.count() == 0:
        resb = pickle.loads(tresult[0]['result'].encode())
        row['tecoresult_task_id']=resb['task_id']
print output
# mod_weather is a dictionary, acceptable parameters T_air, Q_air, Wind_speed,Precip, Pressure, R_global_in, R_longwave_in, CO2
# accepts a list of tuples [(operator,value)]
# Operators add, multiply, subtract, divide, * , - , /  
# + does not work for some reason.Correction + does work but report removes from paramters
#examples {'T_air':[('add',1)]} 
#         {'T_air':[('multiply',0.5),('add',10)]}
