import os
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import StandardScaler
from utils.timefeatures import time_features
import warnings

warnings.filterwarnings('ignore')

class Dataset_Stock_Price(Dataset):
    def __init__(self, root_path, size, flag='train', features='MS', target='close'):
        self.seq_len = size[0]
        self.pred_len = size[2]
        
        self.df_list = []
        self.df_index = []
        #import pdb; pdb.set_trace()
        csv_files = []
        for root, dirs,files in os.walk(root_path):
            for file in files:
                if file.lower().endswith(".csv"):
                    csv_files.append(os.path.join(root, file))
        
        csv_files.sort()
        for file in csv_files:
            df_this = pd.read_csv(file).iloc[::-1]
            df_this = df_this[['date', 'open', 'high', 'low', 'close']]
            data = df_this.values
            self.df_list.append(data)
            if len(df_this) < self.seq_len + self.pred_len:
                continue
            for i in range(len(data)-self.pred_len):
                self.df_index.append([len(self.df_list)-1, i])
        #self.data_x = data[0: len(df_raw)-self.seq_len-self.pred_len]
        #self.data_y = data[0: len(df_raw)-self.seq_len-self.pred_len]
    

    def __getitem__(self, index):
        index_1 = self.df_index[index][0]
        data = self.df_list[index_1]
        
        index_2 = self.df_index[index][1]

        s_begin = index_2
        s_end = s_begin + self.seq_len

        r_begin = s_end
        r_end = r_begin + self.pred_len

        seq_x = data[s_begin:s_end]
        new_x_columns = np.ones((len(seq_x), 4), dtype=float)
        seq_x = np.hstack((seq_x, new_x_columns)) 
        for i in range(len(seq_x)):
            seq_x[i][5] = (seq_x[i][1]/seq_x[0][1]-1)*100
            seq_x[i][6] = (seq_x[i][2]/seq_x[0][1]-1)*100
            seq_x[i][7] = (seq_x[i][3]/seq_x[0][1]-1)*100
            seq_x[i][8] = (seq_x[i][4]/seq_x[0][1]-1)*100
        

        seq_y = data[r_begin:r_end]

        return seq_x, seq_y

    def __len__(self):
        return len(self.df_index)
 
    #def __getitem__(self, index):
    #    #import pdb
    #    #pdb.set_trace()
    #    s_begin = index
    #    s_end = s_begin + self.seq_len

    #    r_begin = s_end
    #    r_end = r_begin + self.pred_len

    #    seq_x = self.data_x[s_begin:s_end]
    #    seq_y = self.data_y[r_begin:r_end]

    #    return seq_x, seq_y        

    #def __len__(self):
    #    #return len(self.data_x) - self.seq_len - self.pred_len + 1
    #    return len(self.data_x)
