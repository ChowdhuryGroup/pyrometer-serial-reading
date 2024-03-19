#written by Zhihan on 2024-03-16 Github uploaded
#loop finding breakpoint for eheating fitting
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sympy as sp
from scipy.interpolate import interp1d
import os
import csv

breakpoint=[4.5e-9,2e-7] #initialize in main code, changed by calling function;
breakpoint=sorted(breakpoint)
def sort_lists(PDcurrent,T):
    sorted_lists = sorted(zip(PDcurrent, T)) #use sorted pdcurrent index sort T
# Unpack the sorted lists
    PDcurrent, T = zip(*sorted_lists)
    return PDcurrent,T

def fraction_generate(PDcurrent,T,breakpoint):
    T_fraction={}
    PDcurrent_fraction={}
    for j in range(len(T)):
        if not breakpoint:
            T_fraction['all']=T
            PDcurrent_fraction['all']=PDcurrent
        for i in range(len(breakpoint) - 1):
            if breakpoint[i] <= PDcurrent[j]<= breakpoint[i + 1]:
                if all(f'{breakpoint[i]} <= PDcurrent[j]< {breakpoint[i + 1]}' not in d for d in PDcurrent_fraction):
                    PDcurrent_fraction[f'{breakpoint[i]} <= PDcurrent[j]< {breakpoint[i + 1]}']=[PDcurrent[j]]
                    
                    T_fraction[f'{breakpoint[i]} <= PDcurrent[j]< {breakpoint[i + 1]}']=[T[j]]
                    
                else:
                    PDcurrent_fraction[f'{breakpoint[i]} <= PDcurrent[j]< {breakpoint[i + 1]}'].append(PDcurrent[j])
                    T_fraction[f'{breakpoint[i]} <= PDcurrent[j]< {breakpoint[i + 1]}'].append(T[j])
            
        if PDcurrent[j]<breakpoint[0]:
            if all(f' PDcurrent[j]< {breakpoint[0]}' not in d for d in PDcurrent_fraction):
                PDcurrent_fraction[f' PDcurrent[j]< {breakpoint[0]}']=[PDcurrent[j]]
                
                T_fraction[f' PDcurrent[j]< {breakpoint[0]}']= [T[j]]
               
            else:
                PDcurrent_fraction[f' PDcurrent[j]< {breakpoint[0]}'].append(PDcurrent[j])
                T_fraction[f' PDcurrent[j]< {breakpoint[0]}'].append(T[j])
        elif PDcurrent[j]>breakpoint[-1]:
            if all(f'PDcurrent[j]> {breakpoint[-1]}' not in d for d in PDcurrent_fraction):
                PDcurrent_fraction[f'PDcurrent[j]> {breakpoint[-1]}']=[PDcurrent[j]]
                
                T_fraction[f'PDcurrent[j]> {breakpoint[-1]}']=[T[j]]
                
            else:
                PDcurrent_fraction[f'PDcurrent[j]> {breakpoint[-1]}'].append(PDcurrent[j])
                T_fraction[f'PDcurrent[j]> {breakpoint[-1]}'].append(T[j])
    return PDcurrent_fraction,T_fraction

def breakpoint_check(T_catalog,PDcurrent_catalog):
    global breakpoint
    degree=4
    T_solution_catalog=[]
    coefficientsT_catalog = np.polyfit(T_catalog, PDcurrent_catalog,degree)
    poly_function_catalog = np.poly1d(coefficientsT_catalog)
    for i in range(len(PDcurrent_catalog)):
        f_catalog = interp1d(poly_function_catalog(T_catalog), T_catalog,fill_value='extrapolate')
        solutions_catalog=f_catalog(PDcurrent_catalog[i])
        T_solution_catalog.append(solutions_catalog)
    T_difference_catalog=np.subtract(T_catalog,T_solution_catalog)
    for j in range(len(T_difference_catalog)):
        if T_difference_catalog[len(T_difference_catalog)-1-j]>=50:
            if PDcurrent_catalog[j] not in breakpoint:
               breakpoint.append(PDcurrent_catalog[j])
               breakpoint=sorted(breakpoint)
    return breakpoint

def sec_fitting_generate(PDcurrent_catalog,T_catalog):
    degree=4
    T_solution_catalog=[]
    coefficientsT_catalog = np.polyfit(T_catalog, PDcurrent_catalog,degree)
    poly_T= np.polyval(coefficientsT_catalog, T_catalog)
    poly_function_catalog = np.poly1d(coefficientsT_catalog)
    for i in range(len(PDcurrent_catalog)):
        f_catalog = interp1d(poly_function_catalog(T_catalog), T_catalog,fill_value='extrapolate')
        solutions_catalog=f_catalog(PDcurrent_catalog[i])
        T_solution_catalog.append(solutions_catalog)
    T_difference_catalog=np.subtract(T_catalog,T_solution_catalog)
    T_error=np.mean(T_difference_catalog ** 2)
    return poly_function_catalog, T_difference_catalog,T_error,poly_T,f_catalog






