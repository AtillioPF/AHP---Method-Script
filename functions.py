##############################################################################################
##                                    Functions File
##############################################################################################
##                            University of Caxias do Sul - UCS
##                        Department of Engineering and Exact Sciences
##
##  Author: Atillio Pinno Fetter
##  Date: May, 2023
##############################################################################################

#### Imports ####
import numpy as np
import matplotlib.pyplot as plt
##############################################################################################
class functions():
    
    @staticmethod
    def get_evaluation_vector_normalized(self, vector, k, position, value):
        k_position = self.get_k_position_index(self, position)
        k += vector[5:]
        vector[k_position] += value
        for c in range(11):
            if k[c] != 0 & c<5:
                vector[c] = vector[c]/k[c]
        return np.array(vector)

    @staticmethod
    def get_evaluation_vector(self, k, position):
        pos = self.get_position_index(position)
        eval_vec = [k[i] if i<5 else 1 if i==pos else 0 for i in range(11)]
        return eval_vec
    
    @staticmethod
    def get_workload(self, w, k):
        size_k = len(k)
        wk = [w[i] if k[i]!=0 else 0 for i in range(size_k)]
        we = np.array(w/sum(wk))
        we = np.transpose(we)
        workload = k @ we
        return workload.real
    
    @staticmethod
    def get_total_workload(self, start, end, k, position, k_position, w):
        total = end-start
        x_axis = []
        workload = []
        for value in range(start, total):
            eval_vec = self.get_evaluation_vector(self, k, position)
            k_matrix = self.get_evaluation_vector_normalized(self, eval_vec, k, k_position, value)
            workload.append(self.get_workload(self, w, k_matrix))
            x_axis.append(value)
        return x_axis, workload

    @staticmethod
    def get_k_position_index(self, k):
        k_pos = k.lower()
        if k_pos == "k1":
            return 0
        if k_pos == "k2":
            return 1
        if k_pos == "k3":
            return 2
        if k_pos == "k4":
            return 3
        if k_pos == "k5":
            return 4
        return None
    
    def get_position_index(self, position):
        pos = position.lower()
        if pos=="adm1/re1":
            return 5
        if pos=="adm2/re2":
            return 6
        if pos=="adm3/re3":
            return 7
        if pos=="adm4/re4":
            return 8
        if pos=="ftt":
            return 9
        if pos=="ptt":
            return 10
        return None

    def pair_comparisson(self,w ,range_dict, k_position, elements_data_list):
        result_list = []
        for element in elements_data_list:
            k = element['k']
            start = range_dict['start']
            end = range_dict['end']
            position = element['position']
            x_axis, workload = self.get_total_workload(self, start, end, k, position, k_position, w)
            result_list.append({'x_axis':x_axis, 'data':workload, 'label':element['position']})
        return result_list

    def plot_graph(self, data, x_limits, y_limits, texts):

        fig = plt.figure()

        # Creating subplot/axes
        ax = fig.add_subplot(111)

        # Setting axes/plot title
        ax.set_title(texts['title'])

        # Setting X-axis and Y-axis limits
        ax.set_xlim(x_limits)
        ax.set_ylim(y_limits)

        # Setting X-axis and Y-axis labels
        ax.set_xlabel(texts['x_label'])
        ax.set_ylabel(texts['y_label'])

        for element in data:
            plt.plot(element['x_axis'], element['data'], label=element['label'])

        plt.grid(True)

        plt.legend()
        plt.show()