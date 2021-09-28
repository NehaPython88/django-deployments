'''
Created on Apr 16, 2019
@author: nehas
'''
import os
import numpy as np
import pandas as pd
pd.set_option('display.max_columns',1000)  
pd.set_option('display.max_rows',1000)  
pd.set_option('display.width',1000) 
#function for products bought by customers
def fillPeopleProducts(purchasingDataFrame):
    name = []
    product = []
    nameList = []
    productList=[]
    dict = {}
    purchases = purchasingDataFrame[['USER_ID','PRODUCT_ID']]
    columns = purchases.columns
    values = purchases.values
    value = []
    # creating the list of names and products and not including duplicates for same name
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
    df = pd.DataFrame(0, columns = product, index = name)#creating matrix with 0 values
    for i in range(len(nameList)):
        x =nameList[i]
        y = productList[i]
        df[y][x]=1# replacing 0 with 1 for the products(from product list) bought by particular customer in namelist

    return (df)

#function for adding category as new column to product dataframe
def reformatProdData(productDataFrame):
    productDataFrame['CATEGORY']=productDataFrame.DESCRIPTION.str.split('(').str.get(1).str.slice(0,-1).str.strip(")")
    productDataFrame['DESCRIPTION'] = productDataFrame.DESCRIPTION.str.split('(').str.get(0)
# matrix for calculating the number of product purchased max time with other product    
def fillProductCoPurchase(purchasingDataFrame):
    peopleProducts = fillPeopleProducts(purchasingDataFrame)
    cols=peopleProducts.columns
    coPurchase = pd.DataFrame(0,columns = cols, index=cols)
    count = 0
    for x in coPurchase.index:
        for y in coPurchase.columns:
            if x != y:# ignoring same product column with same product row
                count = sum(peopleProducts[x]*peopleProducts[y])
            if count != 0:
                coPurchase[y][x]=count # replacing zero with maximum score
   
    return (coPurchase,peopleProducts)

#function for calculating the maximum products bought by customer
def findMostBought(df):
    mostBoughtProducts = []
    count=0
    for x in df.columns:
        countCol = sum(df[x])
        if countCol>count:
            count=countCol #first calculating the maximum score i.e count
       
    for x in df.columns:
        if (sum(df[x])==count):# getting the name of products which has same count
            mostBoughtProducts.append(x)        
 
    return mostBoughtProducts

# function for printing the products
def printRecProducts(productDataFrame, mostBoughtProducts):
    categoryList = []
    descriptionList = []
    dict = {}

    for x in mostBoughtProducts:
        c = productDataFrame[productDataFrame['PRODUCT_ID']==x]['CATEGORY'].iloc[0]
        categoryList.append(c)
        print(c)
        d = productDataFrame[productDataFrame['PRODUCT_ID']==x]['DESCRIPTION'].iloc[0]
        descriptionList.append(d)
        p = productDataFrame[productDataFrame['PRODUCT_ID']==x]['PRICE'].iloc[0]
        dict[c]=(d,p)
    dictSort = sorted(dict.items())# sorting according to key, i.e category name
    print("Suggest one of our most popular products:")
    print(" ")
    for x in dictSort:
        print('In '+str(x[0]).upper()+'--'+str(x[1][0]).strip()+', $'+str(x[1][1]))
# function for getting the list of products which are bought by corresponding products                
def likelyToBuy(coPurchaseDataFrame,productName):   
    bought = []
    count = max(coPurchaseDataFrame[productName][:])      
    prodList = list(coPurchaseDataFrame.index[coPurchaseDataFrame[productName]==count])
    return prodList
#function for print the above list and it's price
def printLikelyToBuy(productDataFrame,productList):
    print("People who bought it were most likely to buy")
    print(" ")
    dict = {}
    categoryList = []
    descriptionList = []
    for x in productList:
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
    
    for x in dictSort:
        print('In '+str(x[0]).upper()+'--'+str(x[1][0]).strip()+', $'+str(x[1][1]))
       
def main():
    initial = os.getcwd()
    folder = input("Please enter name of folder with product and purchase data files:(prod.csv and purchase.csv)")
    if folder == "pdata-tiny":
        subfolder = "pdata-tiny"
    elif folder == "pdata":
        subfolder = "pdata"
    print("Preparing the co-purchase matrix...")
    
    pathPurchase = os.path.join(initial,subfolder,folder,"purchases.csv")
    purchaseDataFrame = pd.read_csv(pathPurchase)
    coPurchase = fillProductCoPurchase(purchaseDataFrame)
    coPurchaseMatrix = coPurchase[0]
    peopleProduct = coPurchase[1]
    pathProduct = os.path.join(initial, folder,subfolder,'prod.csv')
    productDataFrame = pd.read_csv(pathProduct)
    productDataFrame['CATEGORY']=productDataFrame.DESCRIPTION.str.split('(').str.get(1).str.slice(0,-1).str.strip(")")
    productDataFrame['DESCRIPTION'] = productDataFrame.DESCRIPTION.str.split('(').str.get(0)
       
    product = input("Which product was bought? Enter product id or press enter to quit.")
    if product == "":
         print("Bye!")
         exit()
    else:
        while (product != ""):
            count = sum(coPurchaseMatrix[product])
            if count == 0:
                print("[Maximum co-purchasing score is "+str(count)+"]")
                mostBought = findMostBought(peopleProduct)
                print("Recommend with",product.upper(),":",mostBought)
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                printRecProducts(productDataFrame,mostBought)
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            else:    
                print("[Maximum co-purchasing score "+str(max(coPurchaseMatrix[product]))+"]")
                toBuy=likelyToBuy(coPurchaseMatrix,product)
                print("Recommend with",product.upper(),":",toBuy) 
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                printLikelyToBuy(productDataFrame,toBuy)
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            product = input("Which product was bought? Enter product id or press enter to quit.") 
            if product == "":
                print("Bye!")
                exit()
main()              
        
        
    

