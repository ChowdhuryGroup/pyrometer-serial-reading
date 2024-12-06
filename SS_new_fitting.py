#2024-04-16-1326 on SS paddle doubl check after change filament and pyrometer adjust
#new fitting after pyrometer change, this fitting is done on 2024-04-16
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
#from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sympy as sp
from scipy.interpolate import interp1d
import os
import csv
import loop_finding_breakpoint_for_heating_fitting as LL


#first of all plot raw data and see where the ditting diverges

fig,axes=plt.subplots(3,1)

manual_data1 = np.loadtxt("2024-04-16-1326.csv", delimiter=",")
pyro_data1 = np.loadtxt("2024-04-16_13-27-28.tsv", skiprows=1)
interpolated_photocurrent1 = interp1d(pyro_data1[:, 0], pyro_data1[:, 1])
PDcurrent1=interpolated_photocurrent1(manual_data1[:,0])

manual_data = np.loadtxt("2024-03-15_1836.csv", delimiter=",", skiprows=1)
pyro_data = np.loadtxt("2024-03-15_18-34-19.tsv", skiprows=1)
interpolated_photocurrent0 = interp1d(pyro_data[:, 0], pyro_data[:, 1])
PDcurrent0=interpolated_photocurrent0(manual_data[:,0]) 
PDcurrent0=PDcurrent0.tolist()
T0=manual_data[:,1]
T0=T0.tolist()
PDcurrent1=PDcurrent1.tolist()
T1=manual_data1[:,1]
T1=T1.tolist()


T3=[406,450,502,552,601,652,700,750,800,850,902,950,1008,1056,1103]
T3_cool=[1052,1006,957,902,803,750,700,651,598,551,494,449,393]
T4=[399,454,500,551,600,653,699,750,805,849,906,950,1011,1056,1097]
T4_cool=[1061,1008,957,906,852,805,752,701,647,592,541,501,446,396]
T5=[401,450,500,551,600,650,700,751,801,850,900,951,1003,1054]
T5_cool=[1052,1003,950,901,850,800,750,696,652,597,551,498,450,393]
T6=[403,450,501,553,601,653,704,746,799,850,901,951,1002,1051]
T6_cool=[1003,962,902,852,803,750,697,651,596,546,499,453,394]
PDcurrent3=[1.77525e-8,2.80675e-8,5.56953e-8,1.10221e-7,2.09072e-7,3.87858e-7,6.60761e-7,1.10434e-6,1.76813e-6,2.71194e-6,4.06988e-6,5.74161e-6,9.03543e-6,1.33161e-5,1.90013e-5]
PDcurrent3_cool=[1.50227e-5,1.18504e-5,8.59350e-6,5.92678e-6,2.64227e-6,1.54756e-6,9.19012e-7,5.13047e-7,2.58732e-7,1.35260e-7,6.31262e-8,3.65061e-8,1.82756e-8]
PDcurrent4=[1.18749e-8,2.70397e-8,	5.57058e-8,1.15396e-7,2.20379e-7,4.07397e-7,6.85393e-7,1.15571e-6,1.92320e-6,2.78495e-6,4.30656e-6,6.02975e-6,9.03061e-6,1.16513e-5,1.44957e-5]
PDcurrent4_cool=[1.16289e-5,8.45327e-6,5.88618e-6,3.99614e-6,2.54917e-6,1.68080e-6,1.03132e-6,6.03873e-7,3.28133e-7,1.64018e-7,7.84346e-8,4.69219e-8,2.07842e-8,1.00097e-8]
PDcurrent5=[1.25009e-8,2.64694e-8,5.74998e-8,1.17247e-7,2.24294e-7,4.06885e-7,6.84825e-7,1.13122e-6,1.80721e-6,2.72092e-6,4.00680e-6,5.82172e-6,8.24313e-6,1.09492e-5]
PDcurrent5_cool=[1.06253e-5,7.40209e-6,5.15089e-6,3.52955e-6,2.37816e-6,1.54461e-6,9.68695e-7,5.73463e-7,3.57148e-7,1.84072e-7,9.82594e-8,4.50822e-8,2.21447e-8,9.54853e-9]
PDcurrent6=[1.16258e-8,2.41662e-8,5.32675e-8,1.14453e-7,2.10838e-7,3.94944e-7,6.77937e-7,1.03797e-6,1.65891e-6,2.56418e-6,3.82734e-6,5.52972e-6,7.74659e-6,9.80970e-6]
PDcurrent6_cool=[7.08669e-6,5.32557e-6,3.38580e-6,2.30113e-6,1.51004e-6,9.14264e-7,5.32182e-7,3.22380e-7,1.64850e-7,8.58059e-8,4.34540e-8,2.10433e-8,8.10505e-9]

# Indices of elements to delete
old_T=T3+T4+T5+T6+T3_cool+T4_cool+T5_cool+T6_cool
old_pyro=PDcurrent3+PDcurrent4+PDcurrent5+PDcurrent6+PDcurrent3_cool+PDcurrent4_cool+PDcurrent5_cool+PDcurrent6_cool
#old_T=T0
#old_pyro=PDcurrent0
indices_to_delete = [i for i, val in enumerate(old_T) if 400 >= val or val >=850]

print(indices_to_delete,len(old_T),len(old_pyro))

# Delete elements from list1 and list2 at the corresponding indices
for index in sorted(indices_to_delete, reverse=True):
    del old_T[index]
    del old_pyro[index]
print(old_T)
  
    


#PDcurrent=PDcurrent3+PDcurrent4+PDcurrent5+PDcurrent6+PDcurrent3_cool+PDcurrent4_cool+PDcurrent5_cool+PDcurrent6_cool+PDcurrent1
#T=T=T3+T4+T5+T6+T3_cool+T4_cool+T5_cool+T6_cool+T1
PDcurrent=PDcurrent1+PDcurrent0
T=T1+T0


breakpoint=[2e-7]
PDcurrent,T=LL.sort_lists(PDcurrent,T)
PDcurrent_fraction,T_fraction=LL.fraction_generate(PDcurrent,T,breakpoint)
fitted_functions={}
T_differences={}
T_Errors={}
poly_Ts={}
f_catalogs={}
for (PDcurrent_key_list,PDcurrent_list),(T_key_list,T_list) in zip(PDcurrent_fraction.items(), T_fraction.items()):
    sec_fitted_function,T_difference,T_error,poly_T,f_catalog=LL.sec_fitting_generate(PDcurrent_list,T_list)
    fitted_functions[PDcurrent_key_list]=sec_fitted_function
    T_differences[PDcurrent_key_list]=T_difference
    T_Errors[PDcurrent_key_list]=T_error
    f_catalogs[PDcurrent_key_list]=f_catalog
    #print(sec_fitted_function)
    poly_Ts[PDcurrent_key_list]=poly_T
    axes[0].scatter(T_list,PDcurrent_list,label=f'fit region {T_key_list}')
    axes[0].plot(T_list,poly_T,label=f'fit region {T_key_list} with rmse:{np.sqrt(T_error):.2f}C')
    axes[1].scatter(T_list,T_difference,marker='^',label=f'error TC - fitted temp for fitted region {T_key_list}')
    #x=np.linspace(700,1500,50)
    #ax[1].scatter(f_catalog(PDcurrent_list),PDcurrent_list)
    #print(f_catalog(PDcurrent_list),T_list,len(f_catalog(PDcurrent_list)),len(T_list))
axes[0].legend()
axes[0].set_title('eheating fitting on SS paddle')
axes[0].set_xlabel('SS paddle TC temperature/C')
axes[0].set_ylabel('Photodiode current/A')
axes[1].set_xlabel('SS paddle TC temperature/C')
axes[1].set_ylabel('Fitting error/C')
axes[1].set_ylim(-100,100)
#ax1.legend()
#ax1.legend()
#print(f_catalogs)


def fitting_region_split(PDcurrent_point):
    if not breakpoint:
        fitt_fun=f_catalogs['all'](PDcurrent_point)
    else:
        for i in range(len(breakpoint)-1):
            if breakpoint[i]<= PDcurrent_point <= breakpoint[i+1]:
                fitt_fun=f_catalogs[f'{breakpoint[i]} <= PDcurrent[j]< {breakpoint[i + 1]}'](PDcurrent_point)
        if breakpoint[0]>PDcurrent_point:
            fitt_fun=f_catalogs[f' PDcurrent[j]< {breakpoint[0]}'](PDcurrent_point)
        elif PDcurrent_point>breakpoint[-1]:
            fitt_fun=f_catalogs[f'PDcurrent[j]> {breakpoint[-1]}'](PDcurrent_point)
    return fitt_fun


fitted_T=[]
for i in range(len(PDcurrent)):
    #print(PDcurrent_eheating[i])
    fitted_T.append(fitting_region_split(PDcurrent[i]))
T_difference=np.subtract(T,fitted_T)

#axes[1].scatter(T,T_difference,marker='o')
#plt.show()
'''


fig,axes=plt.subplots(3,1)
#ax1=axes[0].twinx()
axes[0].scatter(manual_data1[:,0],manual_data1[:,1], label='SS paddle TC temperature')
axes[0].scatter(pyro_data1[:,0],pyro_data1[:,2],label='old fitted temperature')
axes[0].set_xlabel('Time/s')
axes[0].set_ylabel('SS paddle temeprature/C')
#ax1.scatter(pyro_data1[:,0],pyro_data1[:,1])
axes[0].legend()
plt.show()
'''