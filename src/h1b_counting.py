#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
H1b Data Analysis project 
20181028

@author: catherineshen
"""

import csv
import glob
import os


def get_state_count(file_obj):
    """ Read a H1b data CSV file and generate the certified counts of occupation, state and total cases in the csv
    
    Args:
        file_obj:(str) the H1b data csv readable path
        
    Returns:
        self.occupation_list(dictionary) a dictionary of occupation and their nums
        self.state_list(dictionary) a dictionary of state and their nums
        self.count(int) the total num of certified cases in the files 
        
    """
    csvfile = open(file_obj, newline='') 
    #read csv using csv.DicReader, specify the delimiter is ";"
    reader = csv.DictReader(csvfile, delimiter=';')
    #initial a dictionary that stores state count {state : state total count}
    state_dic = {}   
    #initial a dictionary that stores occupation count {state : state total count}
    occupation_dic = {}
    #state store the total num of certified cases
    count = 0
    for line in reader:
        #status = True if the status is certified
        try:
            #two kinds of headers, "STATUS" before 2015 or "CASE_STATUS" after 2015
            status = line["STATUS"] == "CERTIFIED" 
        except:
            status = line["CASE_STATUS"] == "CERTIFIED"
        
        if status:
            #if the case status is CERTIFIED,then add into the total number
            count += 1 
            try:
                #get the name of the employer state from the specific input csv row
                #EMPLOYER_STATE: the name of the employer state before 2015
                state = line["LCA_CASE_WORKLOC1_STATE"]
            except:
                #LCA_CASE_EMPLOYER_STATE: the name of the employer state after 2015
                state = line["WORKSITE_STATE"]
                
            #get the state dictonary 
            if state not in state_dic:
                state_dic[state] = 1 
            else:
                state_dic[state] += 1 
            #get the name of the soc name before 2015
            try:
                occupation = line['LCA_CASE_SOC_NAME']
            #get the name of the soc name after 2015
            except:
                occupation = line['SOC_NAME']
                
            #get the occupation dictionary 
            if occupation not in occupation_dic:
                occupation_dic[occupation] = 1 
            else:
                occupation_dic[occupation] += 1 
                
    return state_dic, occupation_dic,  count



def get_top10(dict_input , k):
    """
    Given the output of the get_state_count funciton output the sorted top k results [state, num and percentage] or [occupation,and percentage]
    
    Args:
        state_dic: (dicionary) a dictionary of {state: countnum}
        occupation_dic: (dicionary) a dictionary of {occupation: countnum}
        totalnum: (int) total num of the all certified cases
        k : (int) total top num we want to keep
        
    Returns:
        state_list:(list) sorted with top k result with percentage
        occupation_list:(list) sorted with top k result with percentage
    """
    #change input  dictionary to list
    input_list = [[k,v] for k,v in dict_input.items()]
    
    #sort the list first by the key in alphabetical order and then by the value(reversed)
    sorted_input_list = sorted(sorted(input_list, key = lambda x : x[0]), key = lambda x : x[1], reverse = True)  
    
    #only keep top results <= k after filtering
    if len(sorted_input_list) > k:
        
        topk_list = sorted_input_list[:k]
    else:
        topk_list = sorted_input_list
        
    return topk_list



def store_top10(datalist, totalnum, storename, kind):
    """
    Given the output of the top k funciton, store output with all [states, num and percentage] or [occupations, num and percentage] in txt format
    
    Args:
        datalist: (list) a list of [state: countnum] or [occupaton, countnum]
        totalnum: total num of the all certified cases
        storename: (str) the name and directory of the outputfile
        kind : (str) 'states' or 'occupations'
        
    Returns:
        store the output to top_10_occupations.txt file in the outputfolder
        store the output to top_10_states.txt file in the outputfolder
        
    """
    with open(storename,"w") as f:
        #loop over the top 10 and get the result written into txt file
        #if kind = 'status', store header as this
        if kind == 'states':
            header = "TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE"
        else:
        #if kind = 'occupations', store names as follows
            header = "TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE"
        f.write(header + "\n")
        #filter datalist 
        for data in datalist:
            #'occupations' or 'states'get from the datalist
            item = data[0]
            #the num of the 'occupations' or 'states'
            num = str(data[1])
            #change num to the percentage by devided by totalnum
            percent = (100 * data[1])/totalnum 
            #round it to 1 decimal
            rounded_percent = round(percent,1)
            percentage = str(rounded_percent)+"%"
            f.write(item+';'+num+';'+percentage+'\n')
        f.close
  

if __name__ == "__main__":
    try:
        #using built in lib os to read filepath of h1b_counting.py
        current_path = os.path.dirname(os.path.realpath(__file__))
        #get the parent path
        parent_path  = os.path.abspath(os.path.join(current_path, '..'))
        #get the input path
        input_path = os.path.join(parent_path, 'input')
        #get the output path
        output_path = os.path.join(parent_path, 'output')
    except:
        print('Directory not found')
    
    try:
        #get the input csv using glob
        extension = 'csv'
        os.chdir(input_path)
        result = [i for i in glob.glob('*.{}'.format(extension))]
        directory = result[0]
        print('Processing..'+directory)
    except:
        print('file not found error')
        
    try:
        #get counted dict for states and occupations
        state_dic, occupation_dic,  count = get_state_count(directory)
        
    except:
        print('error in get_state_count')
        
    try:
        #get the top10 states list
        s_top10 = get_top10(state_dic , 10)
    except:
        print('error in get_top10 on states')
        
    try:
        #get the top10 occupation list
        o_top10 = get_top10(occupation_dic , 10)
    except:
        print('error in get_state_count on occupations')
    #save to txt file
    try:
        #get the store directory of states
        save_s_directory = os.path.join(output_path, 'top_10_states.txt')
        #get the store directory of occupations
        save_o_directory = os.path.join(output_path, 'top_10_occupations.txt')
        #store the output 
        store_top10(s_top10,count,save_s_directory,'states')
        store_top10(o_top10,count,save_o_directory,'occupations')
    except:
        print('failed to store and save the file')

    print('Process finished')

