##############################################################################################
##                  Undergraduate Thesis 1 - AHP Load Distribution Algorithm
##############################################################################################
##                            University of Caxias do Sul - UCS
##                        Department of Engineering and Exact Sciences
##
##  Author: Atillio Pinno Fetter
##  Date: May, 2023
##############################################################################################
#### Imports ####
import numpy as np
from random import randint
import scipy.linalg as la
import copy
import scipy
import matplotlib.pyplot as plt
from functions import functions
##############################################################################################
#### functions ####


# Definitions
print('-----------------------------------------------------------------------------')
##############################################################################################
# Teaching workload for each position - vector (a)
a = [
        2.0, # Administrative/Researcher 1
        4.0, # Administrative/Researcher 2
        8.0, # Administrative/Researcher 3
        12.0, # Administrative/Researcher 4
        20.0, # Full-time teacher
        30.0 # Part-time teacher
    ]

##############################################################################################
# Workload of postgraduate teaching for each classification vector (c)
c = [
        2.0, # Administrative/Researcher 1
        4.0, # Administrative/Researcher 2
        4.0, # Administrative/Researcher 3
        4.0, # Administrative/Researcher 4
        0.0, # Full-time teacher
        0.0  # Part-time teacher
    ]

##############################################################################################
# Average number of students per undergraduate class (b)
b = 30.0
# Average number of students per postgraduate class (d)
d = 4.0

##############################################################################################
# Calculation of weights for classifications for comparison with the number of credits served.

# Workload of classifications (wfc)
wfc = [a[i]*b + c[i]*d for i in range(6)]

# Weight of classifications for the number of credits served (wcncs).
wcncs = [9,1,1,1,1,1]
for i in range(1,6): # Calculation of weight normalization according to the workload.
    x = (wfc[5]-wfc[0])/(wfc[i]-wfc[0])
    wcncs[i] =  9 - ((9-1)/x)
    #wcncs[i] = round(wcncs[i], 2)
    
print('Workload of classifications for comparison with the credits served.')
print(wfc)
print('Weight of each classification relative to the credits served.')
print(wcncs)
print('-----------------------------------------------------------------------------')

##############################################################################################
# Calculation of the workload of classifications for comparison with the number of classes,
# disciplines, and new disciplines

# Workload of classifications (wfc)
wfc = [a[i] + c[i] for i in range(6)]

# Weight of classifications for the number of classes, disciplines, and new disciplines (wcndnd)
wcndnd = [9,1,1,1,1,1]
for i in range(1,6): # Calculation of weight normalization according to workload
    x = (wfc[5]-wfc[0])/(wfc[i]-wfc[0])
    wcndnd[i] = 9 - ((9-1)/x)
    #wcndnd[i]  = round(wcndnd[i], 2)
    
print('Workload of classifications for comparison with the number of classes, disciplines, and new disciplines.')
print(wfc)
print('Weight of each classification relative to the number of classes, disciplines, and new disciplines.')
print(wcndnd)
print('-----------------------------------------------------------------------------')

##############################################################################################
# Assembly of the Pairwise Comparison Matrix A mxm (m=11)
# Criteria aij where it is the comparison of criterion i with j, (criterion i) / (criterion j)
# Criteria:
# 1 - Number of credits served (nca)
# 2 - Number of classes (nt)
# 3 - Number of disciplines (nd)
# 4 - Number of new disciplines (ndn)
# 5 - Score for other activities (poa)
# 6 - Classification 1 - Administrative/Researcher 1 (r1)
# 7 - Classification 2 - Administrative/Researcher 2 (r2)
# 8 - Classification 3 - Administrative/Researcher 3 (r3)
# 9 - Classification 4 - Administrative/Researcher 4 (r4)
# 10 - Classification 5 - Full-time faculty (ftt)
# 11 - Classification 6 - Part-time faculty (ptt)

# Inicialização da matriz A
A = [[1.0 for x in range(11)] for x in range(11)]

# Each line represents the comparison of the corresponding element with other elements
# Line x is composed of elements resulting from the comparison of x with the elements
# corresponding to each column of the matrix, x/y, x/x, x/w, and so on with the m elements,
# the comparison is made starting from the main diagonal and then the inverted results are
# mirrored along the main diagonal, where every element a(i,j) = 1/a(j,i).

# Line 1 - Number of credits served (nca)
A[0][0] = 1.0 # nca/nca
A[0][1] = 1.0/5 # nca/nt
A[0][2] = 3.0 # nca/nd
A[0][3] = 1.0/9 # nca/ndn
A[0][4] = 1.0/3 # nca/poa
A[0][5] = wcncs[0] # nca/r1
A[0][6] = wcncs[1] # nca/r2
A[0][7] = wcncs[2] # nca/r3
A[0][8] = wcncs[3] # nca/r4
A[0][9] = wcncs[4] # nca/ftt
A[0][10] = wcncs[5] # nca/ptt

# Line 2 - Number of classes (nt)
A[1][1] = 1.0 # nt/nt
A[1][2] = 7.0 # nt/nd
A[1][3] = 1.0/5 # nt/ndn
A[1][4] = 3.0 # nt/poa
A[1][5] = wcndnd[0] # nt/r1
A[1][6] = wcndnd[1] # nt/r2
A[1][7] = wcndnd[2] # nt/r3
A[1][8] = wcndnd[3] # nt/r4
A[1][9] = wcndnd[4] # nt/ftt
A[1][10] = wcndnd[5] # nt/ptt

# Line 3 - Number of disciplines (nd)
A[2][2] = 1.0 # nd/nd
A[2][3] = 1.0/9 # nd/ndn
A[2][4] = 1.0/5 # nd/poa
A[2][5] = 1.0 # nd/r1
A[2][6] = 1.0 # nd/r2
A[2][7] = 1.0 # nd/r3
A[2][8] = 1.0 # nd/r4
A[2][9] = 1.0 # nd/ftt
A[2][10] = 1.0 # nd/ptt

# Line 4 - Number of new disciplines (ndn)
A[3][3] = 1.0 # ndn/ndn
A[3][4] = 3.0 # ndn/poa
A[3][5] = wcndnd[0] # ndn/r1
A[3][6] = wcndnd[1] # ndn/r2
A[3][7] = wcndnd[2] # ndn/r3
A[3][8] = wcndnd[3] # ndn/r4
A[3][9] = wcndnd[4] # ndn/ftt
A[3][10] = wcndnd[5] # ndn/ptt

# Line 5 - Score for other activities (poa)
A[4][4] = 1.0 # poa/poa
A[4][5] = 1.0 # poa/r1
A[4][6] = 3.0 # poa/r2
A[4][7] = 5.0 # poa/r3
A[4][8] = 7.0 # poa/r4
A[4][9] = 8.0 # poa/ftt
A[4][10] = 9.0 # poa/ptt

# Line 6 - Classification 1 - Administrative/Researcher 1 (r1)
A[5][5] = 1.0
A[5][6] = 1.0
A[5][7] = 1.0
A[5][8] = 1.0
A[5][9] = 1.0
A[5][10] = 1.0

# Line 7 - Classification 2 - Administrative/Researcher 2 (r2)
A[6][6] = 1.0
A[6][7] = 1.0
A[6][8] = 1.0
A[6][9] = 1.0
A[6][10] = 1.0

# Line 8 - Classification 3 - Administrative/Researcher 3 (r3)
A[7][7] = 1.0
A[7][8] = 1.0
A[7][9] = 1.0
A[7][10] = 1.0

# Line 9 - Classification 4 - Administrative/Researcher 4 (r4)
A[8][8] = 1.0
A[8][9] = 1.0
A[8][10] = 1.0

# Line 10 - Classification 5 - Full-time faculty (ftt)
A[9][9] = 1.0
A[9][10] = 1.0

# Line 11 - Classification 6 - Part-time faculty (ptt)
A[10][10] = 1.0

# Mirror A along the main diagonal
A = np.array([[1/A[n][m] if m>n else A[m][n] for n in range(11)] for m in range(11)], dtype=float)
A_show = copy.deepcopy(A)
#  Matrix of rounded weights
A_show = np.array([[round(A_show[m][n], 2) for n in range(11)]for m in range(11)], dtype=float)
#A = A_show
print('Matrix of rounded weights, A.')
print(A_show)
print('-----------------------------------------------------------------------------')

##############################################################################################
# Calculation of eigenvectors and eigenvalues

eignvalues, eignvectors = np.linalg.eig(A)
lambda_max = eignvalues.real[0]
eignvectors = np.array(eignvectors)
eignvector = eignvectors[:, 0]
normalized_eignvector = eignvector.real/sum(eignvector.real)
print('Non-zero eigenvalue. {}'.format(lambda_max))
print('Corresponding eigenvector.')
print(normalized_eignvector)
print('-----------------------------------------------------------------------------')

##############################################################################################
#  Consistency Index
ic = (lambda_max - 11)/(11-1)
print('Consistency Index: {}'.format(ic))
print('-----------------------------------------------------------------------------')

##############################################################################################
# Consistency Ratio
rc = ic / 1.51
print('Consistency Ratio: {}'.format(rc))
print("Result: " + ("Consistent" if rc <= 0.1 else "Inconsistent"))
print('-----------------------------------------------------------------------------')

##############################################################################################
# Workload Assessment
########################################################################################################
#                      Table for reference values for each classification
########################################################################################################
############################################ Adm1/Re1 # Adm2/Re2 # Adm3/Re3 # Adm4/Re4 #  FTT  #  PTT  #
########################################################################################################
# Number of disciplines                    #    2     #    2     #    3     #    4     #   4   #   5   #
########################################################################################################
# Number of classes                        #    2     #    2     #    3     #    4     #   5   #   8   #
########################################################################################################
# Undergraduate teaching workload (ge)     #    2     #    4     #    8     #   12     #   20  #   30  #
########################################################################################################
# Postgraduate teaching workload (he)      #    2     #    4     #    4     #    4     #    -  #    -  #
########################################################################################################
# Number of credits served (ne)            #    68    #   136    #   256    #   376    #  600  #  900  #
########################################################################################################
# Score for other activities               #    180   #   160    #   140    #   120    #  100  #   50  #
########################################################################################################
# k1 - Number of credits served (nca)
# k2 - Number of classes (nt)
# k3 - Number of disciplines (nd)
# k4 - Number of new disciplines (ndn)
# k5 - Score for other activities (poa)
w = np.array(eignvector)
w = w/sum(w)
#w = [round(x,2) for x in w]
#w = w.reshape((11,1))
# vetor de avaliação do docente (exemplo)
# k = [ k1/k1, k2/k2, k3/k3, k4/k4, k5/k5, Adm1/Re1, Adm2/Re2, Adm3/Re3, Adm4/Re4, PTT, FTT ]
fc = functions()
# Comparrisson
number_of_extra_classes = False
number_of_extra_courses = False
variation_in_score = False
all_categories = False

# Construction of parameters to calcualte the variation of workload for Adm1/Re1 
k1 = 68; k2 = 2; k3 = 2; k4 = 0; k5 = 180
Adm1_Re1 = {
    'k': [ k1, k2, k3, k4, k5 ],   
    'position' : "Adm1/Re1",
}
# Construction of parameters to calcualte the variation of workload for Adm2/Re2
k1 = 136; k2 = 3; k3 = 3; k4 = 0; k5 = 160
Adm2_Re2 = {
    'k': [ k1, k2, k3, k4, k5 ],
    'position' : "Adm2/Re2",
}
# Construction of parameters to calcualte the variation of workload for Adm3/Re3
k1 = 256; k2 = 3; k3 = 3; k4 = 0; k5 = 140
Adm3_Re3 = {
    'k': [ k1, k2, k3, k4, k5 ],
    'position' : "Adm3/Re3",
}
# Construction of parameters to calcualte the variation of workload for Adm4/Re4 
k1 = 376; k2 = 4; k3 = 4; k4 = 0; k5 = 120
Adm4_Re4 = {
    'k': [ k1, k2, k3, k4, k5 ],
    'position' : "Adm4/Re4",
}
# Construction of paramweters to calcualte the variation of workload for FTT
k1 = 600; k2 = 5; k3 = 4; k4 = 0; k5 = 100
ftt = {
    'k': [ k1, k2, k3, k4, k5 ],
    'position' : "FTT",
}
# Construction of paramweters to calcualte the variation of workload for PTT
k1 = 900; k2 = 8; k3 = 5; k4 = 0; k5 = 50
ptt = {
    'k': [ k1, k2, k3, k4, k5 ],
    'position' : "PTT",
}

elements_data_list = []

if number_of_extra_classes and not all_categories:
    elements_data_list.append(Adm3_Re3)
    elements_data_list.append(ptt)
    range_dict = {'start':-1,'end':2}
    k_position = 'k2'
    # Comparrison vector calculation
    comparisson_result_list = fc.pair_comparisson(w, range_dict, k_position, elements_data_list)
    texts = {
        'title': 'Variation of workload according to the variation of extra classes',
        'y_label': 'Percenctual Workload Variation',
        'x_label': 'Number of extra classes',
    }
    fc.plot_graph(comparisson_result_list, [-1, 2], [0.95, 1.1], texts)

if number_of_extra_courses and not all_categories:
    elements_data_list.append(Adm3_Re3)
    elements_data_list.append(ptt)
    range_dict = {'start':-1,'end':2}
    k_position = 'k3'
    # Comparrison vector calculation
    comparisson_result_list = fc.pair_comparisson(w, range_dict, k_position, elements_data_list)
    texts = {
        'title': 'Variation of workload according to the variation of extra courses',
        'y_label': 'Percenctual Workload Variation',
        'x_label': 'Number of extra courses',
    }
    fc.plot_graph(comparisson_result_list, [-1, 2], [0.95, 1.1], texts)

if variation_in_score and not all_categories:
    elements_data_list.append(Adm3_Re3)
    elements_data_list.append(ptt)
    range_dict = {'start':-20,'end':40}
    k_position = 'k5'
    # Comparrison vector calculation
    comparisson_result_list = fc.pair_comparisson(w, range_dict, k_position, elements_data_list)
    texts = {
        'title': 'Variation of workload according to the variation of extra score',
        'y_label': 'Percenctual Workload Variation',
        'x_label': 'Number of extra score',
    }
    fc.plot_graph(comparisson_result_list, [-20, 40], [0.7, 1.5], texts)

if number_of_extra_classes and all_categories:
    elements_data_list.append(Adm1_Re1)
    elements_data_list.append(Adm2_Re2)
    elements_data_list.append(Adm3_Re3)
    elements_data_list.append(Adm4_Re4)
    elements_data_list.append(ftt)
    elements_data_list.append(ptt)
    range_dict = {'start':-1,'end':2}
    k_position = 'k2'
    # Comparrison vector calculation
    comparisson_result_list = fc.pair_comparisson(w, range_dict, k_position, elements_data_list)
    texts = {
        'title': 'Variation of workload according to the variation of extra classes',
        'y_label': 'Percenctual Workload Variation',
        'x_label': 'Number of extra classes',
    }
    fc.plot_graph(comparisson_result_list, [-1, 2], [0.95, 1.1], texts)

if number_of_extra_courses and all_categories: 
    elements_data_list.append(Adm1_Re1)
    elements_data_list.append(Adm2_Re2)
    elements_data_list.append(Adm3_Re3)
    elements_data_list.append(Adm4_Re4)
    elements_data_list.append(ftt)
    elements_data_list.append(ptt)
    range_dict = {'start':-1,'end':2}
    k_position = 'k3'
    # Comparrison vector calculation
    comparisson_result_list = fc.pair_comparisson(w, range_dict, k_position, elements_data_list)
    texts = {
        'title': 'Variation of workload according to the variation of extra courses',
        'y_label': 'Percenctual Workload Variation',
        'x_label': 'Number of extra courses',
    }
    fc.plot_graph(comparisson_result_list, [-1, 2], [0.95, 1.1], texts)

if variation_in_score and all_categories:
    elements_data_list.append(Adm1_Re1)
    elements_data_list.append(Adm2_Re2)
    elements_data_list.append(Adm3_Re3)
    elements_data_list.append(Adm4_Re4)
    elements_data_list.append(ftt)
    elements_data_list.append(ptt)
    range_dict = {'start':-20,'end':40}
    k_position = 'k5'
    # Comparrison vector calculation
    comparisson_result_list = fc.pair_comparisson(w, range_dict, k_position, elements_data_list)
    texts = {
        'title': 'Variation of workload according to the variation of extra score',
        'y_label': 'Percenctual Workload Variation',
        'x_label': 'Number of extra score',
    }
    fc.plot_graph(comparisson_result_list, [-20, 40], [0.7, 1.5], texts)
