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
        2.0, # Pesquisador 1
        4.0, # Pesquisador 2
        8.0, # Pesquisador 3
        12.0, # Pesquisador 4
        20.0, # Professor de turno parcial
        30.0 # Professor de turno ntegral
    ]

##############################################################################################
# Carga horária de ensino de pós graduação para cada enquadramento vetor (c)
c = [
        2.0, # Pesquisador 1
        4.0, # Pesquisador 2
        4.0, # Pesquisador 3
        4.0,  # Pesquisador 4
        0.0,  # Professor de turno parcial
        0.0  # Professor de turno ntegral
    ]

##############################################################################################
# Número médio de alunos por turma de graduação (b)
b = 30.0
# Número médio de alunos por turma de pós graduação (d)
d = 4.0

##############################################################################################
# Cálculo dos pesos dos enquadramentos para a comparação com o numero de créditos atendidos

# Carga horaria dos enquadramentos (che)
che = [a[i]*b + c[i]*d for i in range(6)]

# Peso dos enquadramentos para o número de creditos atenditos (penca)
penca = [9,1,1,1,1,1]
for i in range(1,6): # cálculo de limiazação dos pesos de acordo com a carga horária
    x = (che[5]-che[0])/(che[i]-che[0])
    penca[i] =  9 - ((9-1)/x)
    #penca[i] = round(penca[i], 2)
    
print('Carga horária dos enquadramentos para a comparação com os créditos atendidos')
print(che)
print('Peso de cada enquadramento relativo aos créditos atendidos')
print(penca)
print('-----------------------------------------------------------------------------')

##############################################################################################
# Cálculo da carga horária dos enquadramentos para a comparação com número de turmas, 
# disciplinas e novas disciplinas

# Carga horaria dos enquadramentos (che)
che = [a[i] + c[i] for i in range(6)]

# Peso dos enquadramentos para o numero de turmas, disciplinas e novas disciplinas (pentdnv)
pentdnv = [9,1,1,1,1,1]
for i in range(1,6): # cálculo de limiazação dos pesos de acordo com a carga horaria
    x = (che[5]-che[0])/(che[i]-che[0])
    pentdnv[i] = 9 - ((9-1)/x)
    #pentdnv[i]  = round(pentdnv[i], 2)
    
print('Carga horária dos enquadramentos para a comparação com o número de turmas, disciplinas e novas disciplilinas')
print(che)
print('Peso de cada enquadramento relativo ao número de turmas, disciplinas e novas disciplilinas')
print(pentdnv)
print('-----------------------------------------------------------------------------')

##############################################################################################
# Montagem da matriz da Comparação de Pares A mxm (m=11)
# Criterios aij onde é a comparação do critério i com o j, (criterio i) / (criterio j)
# Critérios:
# 1 - Número de créditos atendidos (nca)
# 2 - Número de turmas (nt)
# 3 - Número de disciplinas (nd)
# 4 - Número de disciplinas novas (ndn)
# 5 - Pontuação em outras atividades (poa)
# 6 - Enquadramento 1 - Pesquisador 1 (p1)
# 7 - Enquadramento 2 - Pesquisador 2 (p2)
# 8 - Enquadramento 3 - Pesquisador 3 (p3)
# 9 - Enquadramento 4 - Pesquisador 4 (p4)
# 10 - Enquadramento 5 - Docente de tempo integral (dti)
# 11 - Enquadramento 6 - Docente de tempo parcial (dtp)

# Inicialização da matriz A
A = [[1.0 for x in range(11)] for x in range(11)]

# Cada linha é a comparação do elemento correspondente a linha com os outros elementos
# linha x sera composta por elementos frutos da comparação de x com os elementos 
# correspondentes a cada coluna da matriz, x/y, x/x, x/w e assim por diante com os m elementos,
# a comparação é feita a partir da diagona principal e depois os resultados invertidos são 
# espelhados na diagonal principal, onde todo o elemento a(i,j) = 1/a(j,i).

# Linha 1 - Número de créditos atendidos (nca)
A[0][0] = 1.0 # nca/nca
A[0][1] = 1.0/5 # nca/nt
A[0][2] = 1.0/5 # nca/nd
A[0][3] = 1.0/9 # nca/ndn
A[0][4] = 1.0/9 # nca/poa
A[0][5] = 1.0/penca[0] # nca/p1
A[0][6] = 1.0/penca[1] # nca/p2
A[0][7] = 1.0/penca[2] # nca/p3
A[0][8] = 1.0/penca[3] # nca/p4
A[0][9] = 1.0/penca[4] # nca/dti
A[0][10] = 1.0/penca[5] # nca/dtp

# Linha 2 - Número de turmas (nt)
A[1][1] = 1.0 # nt/nt
A[1][2] = 3.0 # nt/nd
A[1][3] = 1.0 # nt/ndn
A[1][4] = 1.0/7 # nt/poa
A[1][5] = 1.0/pentdnv[0] # nt/p1
A[1][6] = 1.0/pentdnv[1] # nt/p2
A[1][7] = 1.0/pentdnv[2] # nt/p3
A[1][8] = 1.0/pentdnv[3] # nt/p4
A[1][9] = 1.0/pentdnv[4] # nt/dti
A[1][10] = 1.0/pentdnv[5] # nt/dtp

# Linha 3 - Número de disciplinas (nd)
A[2][2] = 1.0 # nd/nd
A[2][3] = 1.0/7 # nd/ndn
A[2][4] = 1.0/5 # nd/poa
A[2][5] = 1.0/pentdnv[0] # nd/p1
A[2][6] = 1.0/pentdnv[1] # nd/p2
A[2][7] = 1.0/pentdnv[2] # nd/p3
A[2][8] = 1.0/pentdnv[3] # nd/p4
A[2][9] = 1.0/pentdnv[4] # nd/dti
A[2][10] = 1.0/pentdnv[5] # nd/dtp

# Linha 4 - Número de disciplinas novas (ndn)
A[3][3] = 1.0 # ndn/ndn
A[3][4] = 1.0 # ndn/poa
A[3][5] = 1.0/pentdnv[0] # ndn/p1
A[3][6] = 1.0/pentdnv[1] # ndn/p2
A[3][7] = 1.0/pentdnv[2] # ndn/p3
A[3][8] = 1.0/pentdnv[3] # ndn/p4
A[3][9] = 1.0/pentdnv[4] # ndn/dti
A[3][10] = 1.0/pentdnv[5] # ndn/dtp

# Linha 5 - Pontuação em outras atividades (poa)
A[4][4] = 1.0 # poa/poa
A[4][5] = 1.0 # poa/p1
A[4][6] = 1.0 # poa/p2
A[4][7] = 1.0 # poa/p3
A[4][8] = 1.0 # poa/p4
A[4][9] = 1.0 # poa/dti
A[4][10] = 1.0 # poa/dtp

# Linha 6 - Enquadramento 1 - Pesquisador 1 (p1)
A[5][5] = pentdnv[0]/pentdnv[0] # ndn/p1
A[5][6] = pentdnv[0]/pentdnv[1] # ndn/p2
A[5][7] = pentdnv[0]/pentdnv[2] # ndn/p3
A[5][8] = pentdnv[0]/pentdnv[3] # ndn/p4
A[5][9] = pentdnv[0]/pentdnv[4] # ndn/dti
A[5][10]= pentdnv[0]/pentdnv[5] # ndn/dtp

# Linha 7 - Enquadramento 2 - Pesquisador 2 (p2)
A[6][6] = pentdnv[1]/pentdnv[1] # ndn/p2
A[6][7] = pentdnv[1]/pentdnv[2] # ndn/p3
A[6][8] = pentdnv[1]/pentdnv[3] # ndn/p4
A[6][9] = pentdnv[1]/pentdnv[4] # ndn/dti
A[6][10] =pentdnv[1]/pentdnv[5] # ndn/dtp

# Linha 8 - Enquadramento 3 - Pesquisador 3 (p3)
A[7][7] = pentdnv[2]/pentdnv[2] # ndn/p3
A[7][8] = pentdnv[2]/pentdnv[3] # ndn/p4
A[7][9] = pentdnv[2]/pentdnv[4] # ndn/dti
A[7][10] = pentdnv[2]/pentdnv[5] # ndn/dtp

# Linha 9 - Enquadramento 4 - Pesquisador 4 (p4)pentdnv[2]/pentdnv[2] # ndn/p3
A[8][8] = pentdnv[3]/pentdnv[3] # ndn/p4
A[8][9] = pentdnv[3]/pentdnv[4] # ndn/dti
A[8][10] = pentdnv[3]/pentdnv[5] # ndn/dtp

# Linha 10 - Enquadramento 5 - Docente de tempo integral (dti)
A[9][9] = pentdnv[4]/pentdnv[4] # ndn/dti
A[9][10] = pentdnv[4]/pentdnv[5] # ndn/dtp

# Linha 11 - Enquadramento 6 - Docente de tempo parcial (dtp)
A[10][10] = pentdnv[5]/pentdnv[5] # ndn/dtp

# Espelhamento de A pela diagonal principal
A = np.array([[1/A[n][m] if m>n else A[m][n] for n in range(11)] for m in range(11)], dtype=float)
A_show = copy.deepcopy(A)
# Matriz de pesos arredondados
A_show = np.array([[round(A_show[m][n], 2) for n in range(11)]for m in range(11)], dtype=float)
#A = A_show
print('Matriz de pesos A, arredondados')
print(A_show)
print('-----------------------------------------------------------------------------')

##############################################################################################
# Cálculo dos autovetores e autovalores

eignvalues, eignvectors = np.linalg.eig(A)
lambda_max = eignvalues.real[0]
eignvectors = np.array(eignvectors)
eignvector = eignvectors[:, 0]
normalized_eignvector = eignvector.real/sum(eignvector.real)
print('Autovalor não nulo: {}'.format(lambda_max))
print('Autovetor correspondente:')
print(normalized_eignvector)
print('-----------------------------------------------------------------------------')

##############################################################################################
# Indice de Consistência
ic = (lambda_max - 11)/(11-1)
print('Indice de consistencia: {}'.format(ic))
print('-----------------------------------------------------------------------------')

##############################################################################################
# Razão de Consistência
rc = ic / 1.51
print('Razão de consistencia: {}'.format(rc))
print("Resultado: " + ("Consistente" if rc <= 0.1 else "Inconsistente"))
print('-----------------------------------------------------------------------------')

##############################################################################################
# Avaliação da Carga de Trabalho

##########################################################################################################
#                      Tabela para valores de referência para cada enquadramento                         #
##########################################################################################################
# ############################################ Adm1/Pq1 # Adm2/Pq2 # Adm3/Pq3 # Adm4/Pq4 #  DTI  #  DTP  #
##########################################################################################################
# No de disciplinas                          #    2     #    2     #    3     #     4    #   5   #   5   #
##########################################################################################################
# No de turmas                               #    2     #    2     #    3     #     4    #   4   #   8   #
##########################################################################################################
# Carga horária de ensino de graduação (ge)  #    2     #    4     #    8     #     12   #   20  #   30  #
##########################################################################################################
# Carga horária de ensino de pós-grad. (he)  #    2     #    4     #    4     #     4    #   -   #   -   #
##########################################################################################################
# N de créditos atendidos (ne)               #    68    #   136    #   256    #    376   #  600  #  900  #
##########################################################################################################
# Pontuação em outras atividades             #   180    #   160    #   140    #    120   #  100  #   50  #
##########################################################################################################
w = np.array(eignvector)
w = w/sum(w)
#w = [round(x,2) for x in w]
#w = w.reshape((11,1))
# vetor de avaliação do docente (exemplo)
# k = [ k1/k1, k2/k2, k3/k3, k4/k4, k5/k5, Pq1/Adm1, Pq2/Adm2, Pq3/Adm3, Pq4/Adm4, PTT, FTT ]
fc = functions()
# Construction of paramweters to calcualte the variation of workload for Pq3/Adm3 
k1 = 256; k2 = 3; k3 = 3; k4 = 0; k5 = 140
k = [ k1, k2, k3, k4, k5 ]
start = -1
end = 2
position = "Pq3/Adm3"
k_position = "k3"
x_axis, workload_adm3 = fc.get_total_workload(fc, start, end, k, position, k_position, w)
print(workload_adm3)

# Construction of paramweters to calcualte the variation of workload for FTT
k1 = 900; k2 = 8; k3 = 5; k4 = 0; k5 = 50
k = [ k1, k2, k3, k4, k5 ]
start = -1
end = 2
position = "FTT"
k_position = "k3"
x_axis, workload_ftt = fc.get_total_workload(fc, start, end, k, position, k_position, w)
print(workload_ftt)
fig = plt.figure()

# Creating subplot/axes
ax = fig.add_subplot(111)

# Setting axes/plot title
ax.set_title('An Axes Title')

# Setting X-axis and Y-axis limits
ax.set_xlim([-1, 2])
ax.set_ylim([0.975, 1.05])

# Setting X-axis and Y-axis labels
ax.set_ylabel('Y-Axis Label')
ax.set_xlabel('X-Axis Label')
plt.plot(x_axis, workload_adm3, 'r', x_axis, workload_ftt, 'b')
plt.show()