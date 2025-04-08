import pandas as pd
import os
import re

def remove_quote(x):

    if type(x)==str:
      
            x = x.replace("'","")
       
    return x

def if_empty_columns(columns):
    for column in columns:
        column = column.replace("'","")
        column = column.replace(".","")
        column = column.replace("Unnamed: ","")
        column = re.sub(r'\d+', '', column)
        if column !='':
            return False
    return True

    


def process_table(df):
    if if_empty_columns(df.columns):
        df.columns = df.iloc[0]  # Set the first row as the new column names
        df = df[1:].reset_index(drop=True)
        return NotImplementedError
    df = df.applymap(remove_quote)
    df = df.dropna(axis=1, how='all')
    columns = df.columns
    
    name = []
    for column in columns: 
        column = column.replace('\'','')
        if column.startswith('.') or column == '' or 'Unnamed' in column:
            continue
        name.append(column)
       
    name = ' '.join(name)
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)
    df = df.dropna(how='all').reset_index(drop=True)
    remove_len = round(len(df)/2)
    df = df.iloc[:remove_len-1]
    df = df.dropna(axis=1, how='all')
    df = df.rename(columns={'':'country'})
    
    return name, df

table_map = {}
numbers = [i for i in range(1,11)]
for num in numbers:
    folder = 'part'+str(num)
    filenames = os.listdir(os.path.join('data',folder))
    filenames.remove('analyzeDocResponse.json')
    filenames = sorted(filenames, key=lambda x: int(x[6:-4]))
    for file in filenames:  
        if file == "table-69.csv":
            print('stop')
        table = pd.read_csv(os.path.join('data',folder,file))
        try:
            name, table = process_table(table)
        except:
            print(file)
            print(folder)
        # if name in table_map:          
        #     try:
                
        #         table_map[name] = pd.concat([table_map[name],table], axis = 0)
        #         table_map[name] = table_map[name].iloc[:-1]             
        #     except:
        #         print(name)
        #         print(folder)
                
        else:
            table_map[name] = table


  
