# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 12:59:47 2022

@authors: Josh Miller, Zack Goldblum, Kevin Ramirez Chavez
"""

#Import modules
import os
import sys
import numpy as np
import warnings
from sql_to_df import sql_to_df
from bmes import tempdir

data_filepath = os.path.join(tempdir(), "final_project_sql", "patient_data.sqlite")
data = sql_to_df(data_filepath, " SELECT subject_id, gender, anchor_age, medication, deathtime, first_careunit, icd_code FROM patient_data LIMIT 0,10000")  # use first 10,000 patients

if 'similarity_score' not in data.keys():
    data['similarity_score'] = 0.0

def knearestneighbors(v, x, k=5):
    """
    This function returns the k nearest neighbors ages and subject_id 

    Arguments
    --------
        v (list): list of values to compare x to
        x (int): Number to compare closeness of other values to 
        k (int): Number of nearest neighbors

    Returns
    -------
        outs[0:k] (list): List of k closest values associated to x 
        indices[0:k] (list): List of k subject_id associated with the nearest value
    """

    outs = []
    indices = []
    subject_list = np.array(data['subject_id'])
    if len(v) < k:
        s = np.sort(v) #Return sorted list if v is small enough
        return s
    elif k <= len(v):
        s = np.array(v)
        for i in range(len(v)):
            absdiff = np.abs(s-x) #Take the absolute values of the array
            index = absdiff.argmin() #Get the index of the minimum value in the array
            indices.append(int(subject_list[index])) #Add the subject_id associated with the minimum value to the id array
            outs.append(int(s[index])) #Add the minimum value to the nearest neighbors array
            s = np.delete(s,index) #Remove the minimum value in the original array
            subject_list = np.delete(subject_list, index) #Remove the id associated with the minimum value from the original array
    return outs[0:k], indices[0:k]
    
def similarity_search(age, gender, medication, first_careunit, icd_code, k = 100):
    """
    This function completes a similarity search and returns a predicted survival rate for the patient from the k nearest neighbors

    Arguments
    --------
        age (int): Age of the subject
        gender (str): Sex of the subject (M or F)
        medication (str): Medication prescribed to the subject
        first_careunit (str): The department of a hospital the subject was admitted to
        icd_code (str): String that encodes a medical diagnosis
        k (int): Number of nearest neighbors

    Returns
    -------
        survival_rate (float): Percentage of the number of k nearest subjects who did not die 
        high_subjects (list): Returns the subject_id of the k highest similarity_scores
    """
    
    #Silence warnings from pandas 
    warnings.filterwarnings('ignore')
    
    #Define how much matching parameters affect similarity_score
    age_weight = 0.3
    gender_weight = 0.1
    medication_weight = 0.5
    first_careunit_weight = 0.8
    icd_code_weight = 1 
    
    #Change similarity score in all values to 0
    #Used as failsafe to ensure each similarity_score starts equally
    for i in range(len(data)):
         data['similarity_score'][i] = 0.0
       
    #Compare age and get increase k nearest similarity scores by AGE_WEIGHT
    age_sim = data['anchor_age'] #Makes sure all values are usable 
    #age_list, id_list = knn.knearestneighbors(age_sim, age, 5) #Get k nearest ages and the ids associated with the subjects with those ages
    age_list, id_list = knearestneighbors(age_sim, age, k) #Get k nearest ages and the ids associated with the subjects with those ages

    #Loop through list with id of k nearest ages and increase their respective similarity_score by AGE_WEIGHT
    for i in range(len(id_list)):
        for j in range(len(data)):
            if data['subject_id'][j] == id_list[i]:
                data['similarity_score'][j] += age_weight                
    
    #Compare gender and increase similarity score by GENDER_WEIGHT
    for i in range(len(data)):
        if data['gender'][i] == gender:
            data['similarity_score'][i] += gender_weight 
        
    #If medication, first_careunit, deathtime, icd_code is a string convert to list
    #This makes it possible to iterate through each value
    for i in range(len(data)):   
        if type(data['medication'][i]) == str:
            data['medication'][i] = data['medication'][i].split(',')
        if type(data['first_careunit'][i]) == str:
            data['first_careunit'][i] = data['first_careunit'][i].split(',')
        if type(data['deathtime'][i]) == str:
            data['deathtime'][i] = data['deathtime'][i].split(',')
        if type(data['icd_code'][i]) == str:
            data['icd_code'][i] = data['icd_code'][i].split(',')
    
    #Check if medication, first_careunit, deathtime, icd_code values are unique
    for i in range(len(data)):
        data['medication'][i] = np.unique(data['medication'][i])
        data['first_careunit'][i] = np.unique(data['first_careunit'][i])
        data['deathtime'][i] = np.unique(data['deathtime'][i])
        data['icd_code'][i] = np.unique(data['icd_code'][i])
        
    #Compare medications and increase similarity score by MEDICATION_WEIGHT
    for i in range(len(data)):
        for j in range(len(data['medication'][i])):
            if data['medication'][i][j] == medication:
                data['similarity_score'][i] += medication_weight

    #Compare first_careunit and increase similarity score by FIRST_CAREUNIT_WEIGHT
    for i in range(len(data)):
        for j in range(len(data['first_careunit'][i])):
            if data['first_careunit'][i][j] == first_careunit:
                data['similarity_score'][i] += first_careunit_weight
    
    #Compare icd_code and increase similarity score by 1 
    for i in range(len(data)):
        for j in range(len(data['icd_code'][i])):
            if data['icd_code'][i][j] == icd_code:
                data['similarity_score'][i] += icd_code_weight
                    
    #Get subject_id of the k highest similarity scores
    sim_high_score = []
    sim_scores = []
    high_subjects = []
    subject_list = np.array(data['subject_id'])
    
    #Store all similarity scores in an array 
    for i in range(len(data)):
        sim_scores.append(data['similarity_score'][i])
    sim_scores = np.array(sim_scores)
    
    #Loop through sim_scores to get k highest similarity scores
    for i in range(k):
        index = sim_scores.argmax() #Get highest similarity score
        sim_high_score.append(sim_scores[index]) #Add highest similarity score to an array of the highest scores
        sim_scores = np.delete(sim_scores, index) #Remove argmax score from original array
        high_subjects.append(int(subject_list[index])) #Get subject_id at argmax index
        subject_list = np.delete(subject_list, index) #Remove subject with argmax score from subject list
    
    #Check if k nearest subject_id did not die  
    alive = 0
    total = k
    for i in range(len(high_subjects)):
        if len(data['deathtime'][i]) == 1:
            if data['deathtime'][i] == 'None':
                alive += 1
        elif len(data['deathtime'][i]) > 1:
            pass #Do nothing since deaths are not being tracked 

    #Calculate survival rate as the percentage of alive out of total
    survival_rate = round((alive/total)*100, 2)

    return survival_rate, high_subjects