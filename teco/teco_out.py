import re
import string

fa=[]
file=open('TECO_H2O_daily.csv')
lines=file.readlines()
file.close()
for i in lines:
	fa.append(i.split())

fa.remove(['d,P,Tr,E,R,ws,fw,topfw,omega,', 'wc1,wc2,wc3,wc4,wc5,wc6,wc7,wc8,wc9,wc10'])
	
for i in range(14):
	for j in range(365):
		print float(re.sub(',','',fa[j][i]))

