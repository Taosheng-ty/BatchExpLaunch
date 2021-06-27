
import glob
import os
import pandas as pd
import json
import matplotlib.pyplot as plt 
from progressbar import progressbar
def read_json(file_path):
    with open(file_path,"r") as f:
        result=json.load(f)
    return result
def find_max_len(result):
    length=1
    for i in result.keys():
        length=max(length,len(result[i]))
    return length
def append_single(result,max_len):
    for i in result.keys():
        if len(result[i])<max_len:
            result[i]=result[i]+[result[i][-1]]*(max_len-len(result[i]))
def write_back(result,file_path):
    with open(file_path,"w") as f:
        json.dump(result,f)
def get_path_sets(root_path):
    paths=glob.glob(root_path+'/**/*.jjson', recursive=True)
    path_sets=set()
    for path in paths:
        path_root=os.path.join(*path.split("/")[:-2])
        # result_cur=read_json(path)
        # max_len=find_max_len(result_cur)
        # append_single(result_cur,max_len)
        # write_back(result_cur,path)
        # print(result_cur)
        # print(path_root)
        path_sets.add(path_root)
    return path_sets
def merge_single_experiment_results(root_path):
    paths=glob.glob(root_path+'/**/*.jjson', recursive=True)
    # print(paths)
    df_result_cur=pd.DataFrame()
    for path in paths:
        pd_frame=pd.read_json(path)
        df_result_cur=df_result_cur.append(pd_frame)
    return df_result_cur

def merge_multiple_experiment_results(root_path):
    path_sets=get_path_sets(root_path)
    for path_set in progressbar(path_sets):
        df_result_cur=merge_single_experiment_results(path_set)
        df_result_cur.to_csv(path_set+"/result.ccsv")

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value
def get_node(root_path,path):
    all_node=path.split("/")
    start_folder=root_path.split("/")[-1]
    ind=all_node.index(start_folder)
    start_node=all_node[ind+1:]
    return start_node
def set_node_val(node_list,multi_level_dict,val):
    for i in node_list[:-1]:
        multi_level_dict=multi_level_dict[i]
    last_node=node_list[-1]
    multi_level_dict[last_node]=val
def get_result_df(root_path):
    path_sets=get_path_sets(root_path)
    result=AutoVivification()
    for path_set in path_sets:
        node=get_node(root_path,path_set)
        
        result_cur=merge_single_experiment_results(path_set)
        set_node_val(node,result,result_cur)
        # print(result_cur,path_set)
    return result

import itertools

def plot_metrics(name_results_pair:dict,plots_y_partition:str="metrics_NDCG",
plots_x_partition:str="iterations",groupby="iterations",graph_param=None)->None:
    
    '''    
        name_results_pair:{method_name:result_dataframe}
        plots_partition: key name in each result_dataframe which need to be plotted
    '''
    
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors_list = prop_cycle.by_key()['color']
    colors=itertools.cycle(colors_list)
    marker = itertools.cycle((',', '+', '.', 'o', '*')) 
    for algo_name in name_results_pair:
            algo_result=name_results_pair[algo_name]
            mean=algo_result.groupby(groupby).mean().reset_index()
            std=algo_result.groupby(groupby).std().reset_index()
            assert plots_y_partition in algo_result, algo_name+" doesn't contain the partition "+plots_y_partition
            # if "iteration" in algo_result:
            plt.plot(mean[plots_x_partition],mean[plots_y_partition], marker = next(marker),color=next(colors), label=algo_name)
            # else:
            #     plt.axhline(algo_result[plots_y_partition].values[0], marker = next(marker),color=next(colors),label=algo_name)
    gca=plt.gca()
    gca.set(**graph_param)
    plt.legend()