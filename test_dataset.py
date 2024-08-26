from data_provider.data_loader import Dataset_Custom
from data_provider.stock_data_loader import Dataset_Stock_Price


#data_set = Dataset_Custom(root_path="/iTransformer/dataset/traffic", size=[96, 0, 96], features="MS", data_path="traffic.csv", timeenc=1)
#print(len(data_set))
#print(data_set[0])

data_set = Dataset_Stock_Price(root_path="dataset/stock/taobao/TSLA/2022-12/", size=[30,0,30])
#data_set = Dataset_Stock_Price(root_path="dataset/stock/taobao/TSLA_test", size=[30,0,30])
#data_set = Dataset_Stock_Price(root_path="dataset/stock/taobao/TSLA/", size=[30,0,30])
print(len(data_set))
print(data_set[0])

#for i in range(len(data_set.df_index)):
#    print(i, data_set.df_index[i])
