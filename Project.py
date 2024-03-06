

from unicodedata import category
import pyodbc



import matplotlib.pyplot as plt
import pandas as pd

import numpy as np


from sqlalchemy.engine import URL
from sqlalchemy import create_engine





connectionstring = 'DRIVER={ODBC Driver 17 for SQL Server};Server=LAPTOP-I41SLUOP;Database=BikeStores;Trusted_Connection=Yes;'
connectionurl = URL.create("mssql+pyodbc", query={"odbc_connect": connectionstring})
 


engine = create_engine(connectionurl)

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP-I41SLUOP;'
                      'Database=BikeStores;'
                      'Trusted_Connection=yes;')
 
cursor = conn.cursor()



class customer_login:
    
    
    def __init__(self, username, password):
            self.username = username 
            self.password=password
            self.map=""
            self.users = pd.read_sql_query('''  Select * from dbo.Loog11 ;  ''', engine)
            self.users_information = pd.read_sql_query('''  Select * from sales.customers ;  ''', engine)
            self.admins = pd.read_sql_query('''  Select * from dbo.admins ;  ''', engine)
   
   
   
    def add_users(self):
        cursor.execute("insert into dbo.Loog11 (username, password) values ( ?, ?)",
            (self.username, self.password))
        conn.commit()

    
    
    def check_login(self):
        
        self.map = pd.DataFrame(columns=['username','password'])
        self.map=self.map.append(dict(zip(self.map.columns,[self.username,self.password,])), ignore_index=True)
        
        self.df = pd.merge(self.map, self.users, on=['username','password'], how='left', indicator='Exist')
        
        self.df['Exist'] = np.where(self.df.Exist == 'both', True, False)
        
        return self.df['Exist'].item()
    
    
    
    def check_admin_login(self):
        
        self.map = pd.DataFrame(columns=['admin_username','admin_password'])
        self.map=self.map.append(dict(zip(self.map.columns,[self.username,self.password,])), ignore_index=True)
        
        self.df = pd.merge(self.map, self.admins, on=['admin_username','admin_password'], how='left', indicator='Exist')
        
        self.df['Exist'] = np.where(self.df.Exist == 'both', True, False)
        
        return self.df['Exist'].item()
           
    def check_users(self):
         
        
        self.df_usernames_only= self.users['username']
        if self.username in self.df_usernames_only.values:
            return True
        
        
    def print_users (self):
        
        return self.users 
    
    
    
    def print_sales(self):
        self.sales = pd.read_sql_query('''  Select * from dbo.cart11 ;  ''', engine)
        return self.sales
    
    
    def print_purchases(self, username):
        
        self.purchases = pd.read_sql_query('''  Select * from dbo.cart11 ;  ''', engine)
        self.purchases =self.purchases.loc[(self.purchases.username == username) ]
        return self.purchases.loc[:,['product_name','quantity','list_price']]
    
    
    def delete_product(self, product_name): 

        cursor.execute("DELETE FROM production.products WHERE product_name = ?",
        ( product_name))
        conn.commit()      
        
    
    

    

      
    
        
    

class customer (customer_login):
    

    
    
    
    def __init__(self, first_name,last_name,email,street, city,state,zipcode):
        
        
        self.last_name = last_name
        self.state = state
        self.email = email
        self.first_name = first_name
        self.city = city
        self.zipcode= zipcode
        self.street = street
        
    def add_customers_info(self):
        cursor.execute("insert into sales.customers ( first_name,last_name,email,city,street,state,zip_code) values (  ?, ?, ?, ?, ?, ? ,?)",
        ( self.first_name, self.last_name,self.email,self.city,self.street,self.state,self.zipcode))
        conn.commit()
    
        
    
    

class Category:
    def __init__(self):
        self.category_id=''
        self.category_name=''
        self.category_list = pd.read_sql_query('''  Select * from production.categories ;  ''', engine)
        self.product_list = pd.read_sql_query('''   SELECT   category_id,brand_name,product_id, product_name
                                                    FROM     production.products Left Join
                                                    production.brands ON production.products.brand_id = production.brands.brand_id''',engine)
                                                                         
    def print_category_list(self):
        print(' Select category name')
        return self.category_list['category_name']
    
    
    
    def print_brand_list (self,id):
        self.all_data = self.product_list.loc[self.product_list.category_id == id]
        print(' Select Brand name')
        return self.all_data['brand_name'].unique()
    
    
    
    def return_cat_id(self,category_namee):
        self.categories=  self.category_list.loc[ self.category_list.category_name == category_namee]
        self.categories.index = np.arange(1,len(self.categories)+1)
        self.category_name = self.categories['category_name'][1]
        self.category_id = self.categories['category_id'][1]
        return self.category_id
    
class Brand():
    def __init__(self):
           
        self.brand_id=''
        self.brand_name=''
        self.brand_list = pd.read_sql_query('''  Select * from production.brands ;  ''', engine)
        self.product_list = pd.read_sql_query('''  SELECT   category_id,brand_name,product_id, product_name, list_price
                                                    FROM     production.products Left Join
                                                    production.brands ON production.products.brand_id = production.brands.brand_id;''' ,engine)
        
    def return_products(self):
        return self.product_list
    
    def print_product_list (self,cat_id, brand_name):
        self.df_products =self.product_list.loc[(self.product_list.category_id == cat_id) & (self.product_list.brand_name == brand_name)]
        return  self.df_products.loc[:, ['product_name','list_price']]
    
    
    def return_brand_id(self,brand_namee):
        self.brands=  self.brand_list.loc[ self.brand_list.brand_name == brand_namee]
        self.brands.index = np.arange(1,len(self.brands)+1)
        self.brand_name = brand_namee
        self.brand_id = self.brands['brand_id'][1]
        return self.brand_id
    
    
    def chosen_product(self,product_name,brand_name,category_id):
        
        
        self.chosen_products =self.product_list.loc[ (self.product_list.product_name == product_name) & (self.product_list.brand_name == brand_name) & (self.product_list.category_id == category_id)]
        self.chosen_products.index = np.arange(1,len(self.chosen_products)+1)
        
        
            
        return self.chosen_products.loc[:,['product_name','list_price']]
    
    
    def add_to_cart(self, product_name, list_price, user_id):
        cursor.execute("insert into dbo.cart11 ( product_name, list_price, username, quantity) values (?,?, ?, ?)",
        ( product_name, list_price, user_id, quantity))
        conn.commit()  
        
class Product():
    def __init__(self,  product_name,brand_id,category_id,model_year,price):
        
        self.brand_id = brand_id
        self.model_year = model_year
        self.category_id = category_id
        self.product_name=product_name
        self.price=price
    
    
    def add_product(self):
        cursor.execute("insert into production.products (product_name,brand_id,category_id,model_year,list_price) values ( ?,?,?,?, ?)",
            ( self.product_name,self.brand_id, self.category_id, self.model_year, self.price))
        conn.commit()
        





user_admin = input('Press 1 for admin \nPress 2 for customer')
if user_admin == '2':
    
    signup_or_login =input ('For login press 1 \nFor sign up press 2')

    if signup_or_login == '2':
        
        
        print('----------------------------------------------------')
        username = input ('Choose username')
        password = input ('Choose password')
        log = customer_login(username, password)  
        print('----------------------------------------------------')
        
        
        
        while (log.check_users()):
            print('Existing username, please try again')
            username = input ('Choose username')
            password = input ('Choose password')
            log = customer_login(username, password)   
            
        print('----------------------------------------------------')
        first_name = input('Enter your first name')
        last_name = input('Enter your last name')
        email=input('Enter your  email')
        state = input('Enter your  state')
        city= input('Enter your  city')
        zipcode=input('Enter your  zipcode')
        street=input('Enter your  street')
        print('----------------------------------------------------')    
        cust = customer( first_name,last_name,email,street,city,state,zipcode)
            
            
        cust.add_customers_info()
        log.add_users()
            
    if signup_or_login == '1':        
    
        enter_username = input("Enter username")
        enter_password=input("Enter password")
        log=customer_login(enter_username,enter_password)
        
        
        while log.check_login() == False:
        
            print('----------------------------------------------------')
            print('Login Failed, please try again')
            enter_username = input("Enter username")
            enter_password=input("Enter password")
            print('----------------------------------------------------')
            log=customer_login(enter_username,enter_password)
            
        
        
        print('Login Successeful ')
        users=  log.users.loc[ log.users.username == log.username]
        users.index = np.arange(1,len(users)+1)
        print(users)
        users_info=  log.users_information.loc[ log.users_information.customer_id == users['customer_id'][1] ]
        users_info.index = np.arange(1,len(users_info)+1)
        
        print('----------------------------------------------------')
        print('Welcome',users_info['first_name'][1])  
        print('-------------------------------------------------------------')
            
            
            
            
            
            
        while True:
            print('----------------------------------------------------')    
            service_choice = input('Press 1 if you want to see your information \nPress 2 if you want to place an order \nPress 3 to see your previous purchases\nPress 4 if you want to logout')
            print('----------------------------------------------------')  
            if service_choice == '1':
                    
                print(users_info.iloc[:,-(len(users_info.columns) -1):])
                print('-------------------------------------------------------------')
                print('-------------------------------------------------------------')
                print('-------------------------------------------------------------')
                k = input('If you want to go back to service page press 1 \nIf you want to log out press any button')
                if k == '1':
                    continue
                else :
                    print('Logout Successeful')
                    break
                    
                        
            elif service_choice == '2':
                category = Category()
                
                print(category.print_category_list())
                print('-------------------------------------------------------------')
                
            
                category_namE = input('Please select the brand name')
                
                print('-------------------------------------------------------------')
                
                
                
                category.category_id=category.return_cat_id(category_namE)
                
                print(category.print_brand_list(category.return_cat_id(category_namE)))
                
                print('----------------------------------------------------')
                brand_name_input = input('enter Brand name')
                print('----------------------------------------------------')
                brand = Brand()
                
                
                
                
                
                brand.brand_id=brand.return_brand_id(brand_name_input)
                
                print(brand.print_product_list(category.return_cat_id(category_namE),brand_name_input))
                print('----------------------------------------------------')
                product_name_input = input('enter product name')
                print('----------------------------------------------------')
                quantity = input('please enter quantity')
                print('----------------------------------------------------')
                df = brand.chosen_product(product_name_input, brand_name_input, category.return_cat_id(category_namE))
                df.update(df.loc[df['product_name'] == product_name_input,'list_price'].astype(float)*int(quantity))
                print(df)
                
                print('----------------------------------------------------')
                brand.add_to_cart(df['product_name'][1], (df['list_price'][1]), log.username )
                
                k = input('If you want to go back to service page press 1 \nIf you want to log out press any button')
                print('----------------------------------------------------')
                

                if k == '1':
                    continue
                else :
                    print('Logout Successeful')
                    break
            
            elif service_choice == '3':
                
                
                df = log.print_purchases(log.username)
                print(df)
                print('----------------------------------------------------')
                print('Total purchases = ', df['list_price'].sum() )
                print('Total items = ', df['quantity'].sum() )
                print('----------------------------------------------------')
                k = input('If you want to go back to service page press 1 \nIf you want to log out press any button')
                print('----------------------------------------------------')
                
                
            
                if k == '1':
                    continue
                else :
                    print('Logout Successeful')
                    break
            elif service_choice == '4':
                print('Logout Successeful')
                break            

elif user_admin == '1':
    
    
    
    print('----------------------------------------------------')
    username = input ('Choose username')
    password = input ('Choose password')
    log = customer_login(username, password)  
    print('----------------------------------------------------')
    while log.check_admin_login() == False:
        
        print('----------------------------------------------------')
        print('Login Failed, please try again')
        enter_username = input("Enter username")
        enter_password=input("Enter password")
        print('----------------------------------------------------')
        log=customer_login(enter_username,enter_password)
    
    print('Login Successeful')
    print('-------------------------------')
    while True:
        print('----------------------------------------------------')    
        service_choice = input('Press 1 if you want to add a product \nPress 2 if you want to remove a product\nPress 3 to see sales\nPress 4 to see product list\nPress 5 to users list')
        print('----------------------------------------------------')  
        if service_choice == '1':
                    
            product_name = input('Enter product name')
            brand_id= input('Enter brand id')
            category_id= input('Enter category id')
            model_year= input('Enter  modelyear')
            price= input('Enter  price')
            product = Product(product_name,brand_id,category_id,model_year,price)
            product.add_product()
            k = input('If you want to go back to service page press 1 \nIf you want to log out press any button')
            print('----------------------------------------------------')
            if k == '1':
                continue
            else :
                print('Logout Successeful')
                break   
        if service_choice == '2':
           
            product_name = input('enter product name')
            log.delete_product(product_name)
            k = input('If you want to go back to service page press 1 \nIf you want to log out press any button')
            print('----------------------------------------------------')
            if k == '1':
                continue
            else :
                print('Logout Successeful')
                break   
        
        if service_choice == '3':
            print(log.print_sales())
            k = input('If you want to go back to service page press 1 \nIf you want to log out press any button')
            print('----------------------------------------------------')
            if k == '1':
                continue
            else :
                print('Logout Successeful')
                break   
        if service_choice == '4':
            
            brand = Brand()
            print(brand.return_products())
            k = input('If you want to go back to service page press 1 \nIf you want to log out press any button')
            print('----------------------------------------------------')
            if k == '1':
                continue
            else :
                print('Logout Successeful')
                break   
        
        if service_choice == '5':
            
            print(log.print_users())
            k = input('If you want to go back to service page press 1 \nIf you want to log out press any button')
            print('----------------------------------------------------')
            if k == '1':
                continue
            else :
                print('Logout Successeful')
                break
