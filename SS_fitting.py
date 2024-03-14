#SS paddle position 2 and #123 on position 3 based fitting
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sympy as sp
from scipy.interpolate import interp1d
import os

fig,ax=plt.subplots(2,1)
T1=[400,450,498,557,595,649,699,752,795,845,898,949,1005,1054]
p1=[35,40,41,44,44.5,47.5,49,50,51.5,52.5,54.5,56,56.2,54]
T1_cool=[799,753,704,661,606,558,502,463,403]
p1_cool=[50,49.5,48.5,46.5,45.5,44.5,41,39.1,35.2]
T2=[400,450,500,550,599,651,700,750,801,850,900,950,1002,1059,1097]
p2=[34.8,36.5,39.2,40.5,41.8,42.8,43.7,45.6,48,50,50.5,50.5,51,52,49]
T2_cool=[1056,1002,952,902,851,795,794,797,799,800,752,701,652,601,552,494,449,395]
p2_cool=[42.8,38.7,34.8,32.3,29.2,37.4,42.4,45.1,46.6,46.6,45.6,43.7,41.9,41.4,40.5,38.3,36.5,34]
T3=[406,450,502,552,601,652,700,750,800,850,902,950,1008,1056,1103]
p3=[34.8,35.6,37.4,39.5,40.5,41.8,42.8,43.7,45.1,46.6,48.5,50,49,49,50.5]
T3_cool=[1052,1006,957,902,803,750,700,651,598,551,494,449,393]
p3_cool=[48.5,42.8,40.9,36.7,33.2,29.2,28.4,26.3,39.2,38.3,36.5,35.6,32.3]
T4=[399,454,500,551,600,653,699,750,805,849,906,950,1011,1056,1097]
p4=[32.8,35.6,36.5,38.3,40.5,40.9,42.3,43.3,45.1,46.6,48.5,50,49,49,50]
T4_cool=[1061,1008,957,906,852,805,752,701,647,592,541,501,446,396]
p4_cool=[48.5,44.7,41.4,37,34.4,32.3,30.3,29.9,27.3,26.1,34,35.2,34.4,32.3]
T5=[401,450,500,551,600,650,700,751,801,850,900,951,1003,1054]
p5=[32.7,35.2,36.5,37.8,40,40.9,42.8,43.6,45.1,47,48.5,48.5,50.5,50]
T5_cool=[1052,1003,950,901,850,800,750,696,652,597,551,498,450,393]
p5_cool=[46.6,43.7,40.9,38.3,36.1,34.4,32.8,30.3,30.3,28,26.1,24.3,26.5,25.8]
T6=[403,450,501,553,601,653,704,746,799,850,901,951,1002,1051]
p6=[31.1,33.9,35.2,36.9,38.2,40,40.9,42.8,44.1,45.6,48,50,50,48.5]
T6_cool=[1003,962,902,852,803,750,697,651,596,546,499,453,394]
p6_cool=[42.3,40.9,38.7,36.1,35.2,32.7,30.7,28.7,27.2,24.7,23.4,22.2,22.2]
PDcurrent1=[8.74009e-9,1.06121e-8,1.29117e-8,1.77340e-8,2.25961e-8,3.30717e-8,4.68291e-8,6.91074e-8,9.28120e-8,1.29248e-7,1.76090e-7,2.35256e-7,3.22600e-7,4.22586e-7]
PDcurrent1_cool=[7.82051e-8,5.72333e-8,4.05147e-8,2.99040e-8,2.11991e-8,1.56507e-8,1.20525e-8,1.04215e-8,8.77546e-9]
PDcurrent2=[9.22805e-9,1.10551e-8,1.32769e-8,1.73167e-8,2.49161e-8,3.56462e-8,5.21708e-8,7.31495e-8,1.05393e-7,1.49639e-7,1.98966e-7,2.44103e-7,3.24677e-7,4.38107e-7,4.98511e-7]
PDcurrent2_cool=[3.40556e-7,2.48004e-7,1.76694e-7,1.28240e-7,9.06696e-8,5.87833e-8,5.97776e-8,6.27065e-8,6.08344e-8,6.08344e-8,4.29786e-8,2.95552e-8,2.05213e-8,1.45240e-8,1.07284e-8,8.15618e-9,6.98141e-9,5.85423e-9]
PDcurrent3=[1.77525e-8,2.80675e-8,5.56953e-8,1.10221e-7,2.09072e-7,3.87858e-7,6.60761e-7,1.10434e-6,1.76813e-6,2.71194e-6,4.06988e-6,5.74161e-6,9.03543e-6,1.33161e-5,1.90013e-5]
PDcurrent3_cool=[1.50227e-5,1.18504e-5,8.59350e-6,5.92678e-6,2.64227e-6,1.54756e-6,9.19012e-7,5.13047e-7,2.58732e-7,1.35260e-7,6.31262e-8,3.65061e-8,1.82756e-8]
PDcurrent4=[1.18749e-8,2.70397e-8,	5.57058e-8,1.15396e-7,2.20379e-7,4.07397e-7,6.85393e-7,1.15571e-6,1.92320e-6,2.78495e-6,4.30656e-6,6.02975e-6,9.03061e-6,1.16513e-5,1.44957e-5]
PDcurrent4_cool=[1.16289e-5,8.45327e-6,5.88618e-6,3.99614e-6,2.54917e-6,1.68080e-6,1.03132e-6,6.03873e-7,3.28133e-7,1.64018e-7,7.84346e-8,4.69219e-8,2.07842e-8,1.00097e-8]
PDcurrent5=[1.25009e-8,2.64694e-8,5.74998e-8,1.17247e-7,2.24294e-7,4.06885e-7,6.84825e-7,1.13122e-6,1.80721e-6,2.72092e-6,4.00680e-6,5.82172e-6,8.24313e-6,1.09492e-5]
PDcurrent5_cool=[1.06253e-5,7.40209e-6,5.15089e-6,3.52955e-6,2.37816e-6,1.54461e-6,9.68695e-7,5.73463e-7,3.57148e-7,1.84072e-7,9.82594e-8,4.50822e-8,2.21447e-8,9.54853e-9]
PDcurrent6=[1.16258e-8,2.41662e-8,5.32675e-8,1.14453e-7,2.10838e-7,3.94944e-7,6.77937e-7,1.03797e-6,1.65891e-6,2.56418e-6,3.82734e-6,5.52972e-6,7.74659e-6,9.80970e-6]
PDcurrent6_cool=[7.08669e-6,5.32557e-6,3.38580e-6,2.30113e-6,1.51004e-6,9.14264e-7,5.32182e-7,3.22380e-7,1.64850e-7,8.58059e-8,4.34540e-8,2.10433e-8,8.10505e-9]

e1=[0,0,0,0,5,7,12,14,21,29,36,46,65,80]
e1_cool=[19,14.5,12,9,5,0,0,0,0]
e2=[0,0,2,4,6,8,13,16,23,31,39,47,62,84,98]
e2_cool=[75,64,50,40,31,25,20,24,22,22,16,13,9,6,4,2,0,0]
e3=[0,0,1,3,4,7,11,15,19,26,35,47,61,79,98]
e3_cool=[82,70,57,44,25,18,14,11,6,3,2,0,0]
e4=[0,0,2,4,6,8,12,17,23,30,42,52,68,83,140]
e4_cool=[90,74,57,45,32,26,19,14,11,7,4,2,0,0]
e5=[0,0,1,3,5,8,11,16,22,30,40,53,66,84]
e5_cool=[88,73,56,43,33,25,18,14,11,7,6,3,2,0]
e6=[0,0,2,4,6,9,12,16,22,30,41,54,68,83]
e6_cool=[68,57,42,33,25,18,14,11,7,5,3,2,1]

degree=4
T=T3+T4+T5+T6+T3_cool+T4_cool+T5_cool+T6_cool
PDcurrent=PDcurrent3+PDcurrent4+PDcurrent5+PDcurrent6+PDcurrent3_cool+PDcurrent4_cool+PDcurrent5_cool+PDcurrent6_cool
coefficientsT = np.polyfit(T, PDcurrent,degree)

sorted_indices = sorted(range(len(T)), key=lambda i: T[i])

# Use the sorted indices to sort list2
PDcurrent = [PDcurrent[i] for i in sorted_indices]

T=sorted(T)
# Generate y values for the polynomial curve
poly_T = np.polyval(coefficientsT, T)
residuals = PDcurrent-poly_T
poly_function = np.poly1d(coefficientsT)
#print(poly_function)
# Calculate mean squared error (MSE)
mse= np.mean(residuals ** 2)


def write_polynomial(coefficients):
    degree = len(coefficients) - 1
    terms = []

    for i, coef in enumerate(coefficients):
        if i == 0:
            terms.append(f"{coef:.2e}")
        else:
            terms.append(f"{coef:.2e} * x^{i}")

    polynomial = " + ".join(terms)
    return polynomial

x=sp.Symbol('x')
T_solution=[]

# Define the equation
T_inter=T
PDcurrent_inter=PDcurrent
for i in range(len(PDcurrent)):
    f = interp1d(poly_function(T), T,fill_value='extrapolate')
    #print(equation_expr)
    solutions=f(PDcurrent[i])
    #print(solutions)
    T_solution.append(solutions)
T_difference=np.subtract(T_inter,T_solution)
T_error=np.mean(T_difference ** 2)



ax1=ax[1].twinx()
ax1.scatter(T,T_difference,label='offset temperature',color='pink')
ax1.set_ylabel('SS temp - fit temperature /C')
ax1.legend()

ax[1].plot(T,poly_T,marker='^',label=f'fitting:{write_polynomial(coefficientsT)} \n with mse:{mse:.2e} \n with temperature rms-error:{np.sqrt(T_error):.2f}C')

ax[0].plot(p1,e1, marker='o',color='red',label='posiiton 1#1')
ax[0].plot(p1_cool,e1_cool, marker='o',color='salmon',label='cool down posiiton 1#1')
ax[0].plot(p2,e2, marker='o',color='purple',label='posiiton 1#2')
ax[0].plot(p2_cool,e2_cool, marker='o',color='lavender',label='cool down posiiton 1#2')
ax[0].plot(p3,e3, marker='o',color='green',label='posiiton 2')
ax[0].plot(p3_cool,e3_cool, marker='o',color='lightgreen',label='cool down posiiton 2')
ax[0].plot(p4,e4, marker='o',color='black',label='posiiton 3#1')
ax[0].plot(p4_cool,e4_cool, marker='o',color='grey',label='cool down posiiton 3#1')
ax[0].plot(p5,e5, marker='o',color='orange',label='posiiton 3#2')
ax[0].plot(p5_cool,e5_cool, marker='o',color='yellow',label='cool down posiiton 3#2')
ax[0].plot(p6,e6, marker='o',color='brown',label='posiiton 3#3')
ax[0].plot(p6_cool,e6_cool, marker='o',color='tan',label='cool down posiiton 3#3')

ax[0].set_xlabel('filament power/W')
ax[0].set_ylabel('emission current/mA')
ax[0].legend()

ax[1].scatter(T5_cool,PDcurrent5_cool,marker='o',color='yellow',label='cool down posiiton 3 #2')
ax[1].scatter(T5,PDcurrent5,marker='o',color='orange',label='posiiton 3 #2')
ax[1].scatter(T6_cool,PDcurrent6_cool,marker='o',color='tan',label='cool down posiiton 3 #3')
ax[1].scatter(T6,PDcurrent6,marker='o',color='brown',label='posiiton 3 #3')

ax[1].scatter(T4_cool,PDcurrent4_cool,marker='o',color='grey',label='cool down posiiton 3#1')
ax[1].scatter(T4,PDcurrent4,marker='o',color='black',label='posiiton 3#1')
ax[1].scatter(T3_cool,PDcurrent3_cool,marker='o',color='lightgreen',label='cool down posiiton 2')
ax[1].scatter(T3,PDcurrent3,marker='o',color='green',label='posiiton 2')
#ax[1].scatter(T2_cool,PDcurrent2_cool,marker='o',color='lavender',label='cool down posiiton 1#2')
#ax[1].scatter(T2,PDcurrent2,marker='o',color='purple',label='posiiton 1#2')
#ax[1].scatter(T1_cool,PDcurrent1_cool,marker='o',color='salmon',label='cool down posiiton 1#1')
#ax[1].scatter(T1,PDcurrent1,marker='o',color='red',label='posiiton 1#1')
ax[1].set_xlabel('Temperature/C')
ax[1].set_ylabel('photodiode current/A')
#ax[1].set_ylabel('photodiode current/A')
ax[1].set_title('Photodiode current vs SS temperature/pyrometer reading')
ax[1].legend()
#ax[1].set_yscale('log')


#plt.show()

