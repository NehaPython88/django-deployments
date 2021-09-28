import os
import pandas as pd
pd.set_option('display.max_columns',1000)
pd.set_option('display.max_rows',1000)
pd.set_option('display.width',1000)
initial = os.getcwd()
folder = 'pdata-tiny'
subfolder = 'pdata-tiny'
pathProduct = os.path.join(initial, folder,subfolder,'prod.csv')
product = pd.read_csv(pathProduct)
product['CATEGORY']=product.DESCRIPTION.str.split('(').str.get(1).str.slice(0,-1).str.strip(")")
product['DESCRIPTION'] = product.DESCRIPTION.str.split('(').str.get(0) 
mostBought = ['shampoo','teacup']
print(product)
categoryList = []
descriptionList = []
di = {}
print("Suggest one of our most popular products:")
for x in mostBought:
    c = product[product['PRODUCT_ID']==x]['CATEGORY'].iloc[0]
    categoryList.append(c)
    d = product[product['PRODUCT_ID']==x]['DESCRIPTION'].iloc[0]
    descriptionList.append(d)
    p = product[product['PRODUCT_ID']==x]['PRICE'].iloc[0]
    di[c]=(d,p)
    #print("In ", c, " -- ",d,"$",p)
    
    
diSort = sorted(di.items())   
print(diSort)
for x in diSort:
    print('In '+str(x[0])+'--'+str(x[1][0]).strip()+', $'+str(x[1][1]))
    
    
      