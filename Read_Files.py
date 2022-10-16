from multiprocessing.sharedctypes import Value
import os
from tkinter import StringVar
import pandas as pd
import numpy as np
import dask.dataframe as dd
import glob

class ReadCSV():
    def __init__(self, filename = None):
        self.filename = filename
        
    def ReadALLFiles(self,filepath):
        #Import all csv files in the directory
        all_files = glob.glob(self.filepath)
        data_file = []
        for filename in all_files:
            df = pd.read_csv(filename, index_col=None, header=0,encoding='latin-1')
            data_file.append(df)

        raw_df = pd.concat(data_file, axis=0, ignore_index=False)
        
        return raw_df
    
    def main(self):
        while True:
            try:
                filepath = StringVar(input("Enter the Filename or File Folder path and add '.csv' at the back: "))
            except ValueError:
                print("Sorry i dont understand. Please try another input.")
            else:
                break
            
        result = ReadCSV().ReadALLFiles(filepath)
        print(result)
        
if __name__ == '__main__':
    ReadCSV().main()
    
        

# frame.to_csv('test.csv')
