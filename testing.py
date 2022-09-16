# import glob
# import pandas as pd
# import os
    
# #Read all csv file from folder
# path = os.getcwd()
# all_csv_files = glob.glob(os.path.join(path,"instance/uploaded_files/*.csv"))


# # loop over the list of csv files
# for filename in all_csv_files:
#     data_file = []
#     df = pd.read_csv(filename, index_col=None, header=0,encoding='latin-1')
#     data_file.append(df)

#     raw_df = pd.concat(data_file, axis=0, ignore_index=False)
#     # print the location and filename
#     print('Location:', filename)
#     print('File Name:', filename.split("\\")[-1])
    
#     # print the content
#     print('Content:')
#     print()

# from pymongo import MongoClient
# #call default csv from collection
# mongo_client = MongoClient()

# database = mongo_client.Fyp-Test
# collection = database[disney_movies.csv]
# print(collection)