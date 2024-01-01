#go at last to add test case file address/name for running

import pickle
import numpy as np

def Condition_Satisfiability(n,P,Q,k,m,T,M):
    instance_solution = [0]*n 
    ptracker = [0]*P 
    k_sorted = np.argsort(k)
    
    lead_condition = 1
    while lead_condition == 1:
        lead_condition = 0
        for i in k_sorted:
            lead_flag = False
            
            if ptracker[i] == 0:
                
                if k[i] == 0:
                    instance_solution[T[i][0]] = 1
                    ptracker[i] = 1
                else:
                    for idx,j in enumerate(T[i][:-1]):
                        if instance_solution[j] == 0:
                            lead_flag = True
                            break
                    if lead_flag == False:
                        instance_solution[T[i][-1]] = 1 
                        ptracker[i] = 1
                        lead_condition = 1
               
              
    false_must_exist_flag = False
    for q in range(Q):
        temp_q_case = [instance_solution[k] for k in M[q]]
        if all(temp_q_case):
            false_must_exist_flag = True
            break
                 
    return instance_solution if false_must_exist_flag == False else []

def main(name_of_source_file, name_of_solution_file):
    
    datafile  = open(name_of_source_file,'rb')
    data = pickle.load(datafile)
 
    instances = data['numInstances']
    n_list = data['n_list']
    P_list = data['P_list']
    Q_list = data['Q_list']
    k_list = data['k_list']
    m_list = data['m_list']
    T_list = data['T_list']
    M_list = data['M_list']  
    # print(instances)    
    solution = []
   
    for i in range(instances):
        n = n_list[i]
        P = P_list[i]
        Q = Q_list[i]
        k = k_list[i]
        m = m_list[i]
        T = T_list[i]
        M = M_list[i]
        satisfying_soln = Condition_Satisfiability(n,P,Q,k,m,T,M)
        solution.append(satisfying_soln)
        print(f'Complete {i}th instance')

    solution_file = open(name_of_solution_file,'ab')
    pickle.dump(solution,solution_file)
    

#add test case file address in "name_of_source_file" variable below
name_of_source_file = 'examples_of_large_instances'
#add required solution file address in "name_of_solution_file" variable below
name_of_solution_file = 'ashu_examples_of_large_solutions'    
main(name_of_source_file, name_of_solution_file)
print(f'solution file {name_of_solution_file} generated successfully')