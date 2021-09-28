import os
import pandas as pd
import numpy as np
pd.set_option('display.max_columns',1000)
pd.set_option('display.max_rows',1000)
pd.set_option('display.width',1000)
name = []
product = []
nameList = []
productList=[]
dict = {}
initial = os.getcwd()
folder = 'pdata-tiny'
subfolder = 'pdata-tiny'
path = os.path.join(initial, folder ,subfolder,'purchases.csv')
purchases = pd.read_csv(path)
purchases = purchases[['USER_ID','PRODUCT_ID']]
columns = purchases.columns
values = purchases.values
value = []
for i in range(len(purchases)):
    x=(purchases.iloc[i][0])
    if x not in name:
        name.append(x)
        name.sort()
for j in range(len(purchases)):
    y=(purchases.iloc[j][1])
    if y not in product:
        product.append(y)
        product.sort()
for i in range(len(purchases)):
    x=(purchases.iloc[i][0])
    nameList.append(x)
for j in range(len(purchases)):
    y=(purchases.iloc[j][1])
    productList.append(y)
df = pd.DataFrame(0, columns = product, index = name)
for i in range(len(nameList)):
    x =nameList[i]
    y = productList[i]
    df[y][x]=1
        
#print(df)  
count = 0      
cols=df.columns
coPurchase = pd.DataFrame(0,columns = cols, index=cols)

for x in coPurchase.index:
    for y in coPurchase.columns:
        if x != y:
            count = sum(df[x]*df[y])
        if count != 0:
            coPurchase[y][x]=count
#print(coPurchase)
pathProduct = os.path.join(initial, folder,subfolder,'prod.csv')
productDataFrame = pd.read_csv(pathProduct)
productDataFrame['CATEGORY']=productDataFrame.DESCRIPTION.str.split('(').str.get(1).str.slice(0,-1).str.strip(")")
productDataFrame['DESCRIPTION'] = productDataFrame.DESCRIPTION.str.split('(').str.get(0)
    
bought = []
print(coPurchase)
productName = 'bowl'
#print(coPurchase[:][productName])
count = max(coPurchase[productName][:])
#print(coPurchase[:][productName].column[count])
print(count)
prodList = list(coPurchase.index[coPurchase[productName]==count])
#print(prodList)
dict = {}
categoryList = []
descriptionList = []
for x in prodList:
    c = productDataFrame[productDataFrame['PRODUCT_ID']==x]['CATEGORY'].iloc[0]
    categoryList.append(c)
    d = productDataFrame[productDataFrame['PRODUCT_ID']==x]['DESCRIPTION'].iloc[0]
    descriptionList.append(d)
    p = productDataFrame[productDataFrame['PRODUCT_ID']==x]['PRICE'].iloc[0]

    if c not in dict:
        dict[c]=[d,p]  
    else:
        value = dict[c]
        newValue = [d,p]
        value.extend(newValue)
        dict[c]=value
        
dictSort = sorted(dict.items())
print(dictSort)
for x in dictSort:
    print('In '+str(x[0])+'--'+str(x[1][0]).strip()+', $'+str(x[1][1]))
    #print('In '+dictSort.keys()+'--'+dictSort.values().strip()+', $'+str(x[1][1]))
    
