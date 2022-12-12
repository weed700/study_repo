import pandas as pd

e = pd.read_excel('AS500+PD 견적 양식.xlsm',engine='openpyxl',index_col=[2,3,5,6])

name=[]
for temp in e.index:
    name.append(temp[0])

print(set(name))
dic={}

for t in set(name):
    print('start : ',t)
    l_1=[]
    for temp2 in e.index:
        #print('temp: ',temp2[0])
        if t == temp2[0]:
            l_1.append([temp2[1],temp2[2],temp2[3]])
    dic[t] = l_1
    print(dic[t])
    print('*****************')
    

#print(dic['AS500\n일체형'])
#dic={'AS500\n일체형':l_1, 'AS500\nGateway' : l_2}

#print(dic['AS500\n일체형'][1][2])
