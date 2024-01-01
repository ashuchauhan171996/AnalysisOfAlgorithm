#go at last to add test case file address/name for running
import pickle
from collections import defaultdict,deque
import math

def Node_labeler(adjlist,k):
    label = [-1]* len(adjlist)
    seen = [-1]*len(adjlist) 

    parent_labels = defaultdict(dict)
    for n in range(len(adjlist)):
        for m in range(k):
            parent_labels[n][m] = math.inf
    
    
    def path_from_root(des,visited, path,path_storer,adjlist):
        
        if visited[des] == -1:
            visited[des] = 1
            path_storer[des] = path.copy()
            
            for child in adjlist[des]:
                path.append(child)
                path_from_root(child, visited,path, path_storer,adjlist)
                path.pop()
        
 
    path_storer = {}
    visited = [-1]*len(adjlist) 
    path_from_root(0,visited,[0],path_storer,adjlist)
    
    
    def give_label(j):
        nonlocal parent_labels, label
      
        sorted_dict = [k for k, v in sorted(parent_labels[j].items(), key=lambda item: (item[1]), reverse=True)]
        label[j] = sorted_dict[0]
        parent_labels[j][sorted_dict[0]] = 0
        return
    
    def backtrack(j):
        nonlocal parent_labels,label
        
        for i in range(len(path_storer[j])-1,0,-1):
            for p in range(k):
                if p != label[path_storer[j][i-1]]:
                    if parent_labels[path_storer[j][i-1]][p] > parent_labels[path_storer[j][i]][p]:
                        parent_labels[path_storer[j][i-1]][p] = parent_labels[path_storer[j][i]][p] + 1

        return

    
    def forward(j):
        nonlocal parent_labels, label
        
        for i in range(len(path_storer[j])-1):
            
            for p in range(k):
                if p != label[path_storer[j][i+1]]:
                    if parent_labels[path_storer[j][i+1]][p] > parent_labels[path_storer[j][i]][p]:
                        parent_labels[path_storer[j][i+1]][p] = parent_labels[path_storer[j][i]][p] + 1
        return
    
    
    q = deque()
    q.append(0)
    seen[0] = 1
    label[0] = 0
    parent_labels[0][0] = 0
    while q:
        idx = q.popleft()
         
        for j in adjlist[idx]:
            if seen[j] == -1:
                q.append(j)
                seen[j] = 1
                
                forward(j) 
                give_label(j)
                backtrack(j)

                                              
    return label
    

def r_calculator(adjlist, labels, node,k):
    dic = {}
    seen = [-1]*len(adjlist)
    dist = [0]*len(adjlist)   
    hop = 0
    q = deque()
    q.append(node)
    seen[node] = 1
    dic[labels[node]] = 1
    
    if len(dic) == k:
            return hop
        
    while q:
        idx = q.popleft()
        for j in adjlist[idx]:
            if seen[j] == -1:
                q.append(j)
                seen[j] = 1
                dic[labels[j]] = 1
                dist[j] = dist[idx] + 1
        hop = max(dist)
        if len(dic) == k:
            return hop
    return -1   
                
               
def m_calculator(adjlist, labels, node,k):
    seen = [-1]*len(adjlist)
    dist = [0]*len(adjlist)    
    hop = 0
    count = 0
    q = deque()
    q.append(node)
    seen[node] = 1
    count += 1
    
    if count == k:
            return hop
        
    while q:
        idx = q.popleft()
        for j in adjlist[idx]:
            if seen[j] == -1:
                q.append(j)
                seen[j] = 1
                count +=1
                dist[j] = dist[idx] + 1
        hop = max(dist)
        if count >= k:
            return hop
    return -1   
   
    
            
def proximity_ratio_calculator(adjlist, labels, k,i):
    hops = 0
    r_v = [-1]*len(labels)
    m_v = [-1]*len(labels)
    
    
    for node in range(len(labels)):

        r_v[node] = r_calculator(adjlist, labels, node, k)
        m_v[node] = m_calculator(adjlist, labels, node, k)
    
    p_ratio = [r_v[i]/m_v[i] for i in range(len(labels))]
    return p_ratio 

def proximity_ratio_list(adjtree_list,labellings,k_list):
    ratio = []
    instance_ratio = []
    for i in range(len(adjtree_list)):
        p_ratio = proximity_ratio_calculator(adjtree_list[i],labellings[i], k_list[i],i)
        ratio.append(p_ratio)
        instance_ratio.append(max(p_ratio))

    print('\n instance ratio',instance_ratio)
    return ratio
    
   
def main(filename_of_adjlist_of_trees, filename_of_k_values, name_of_solution_file):
    
    datafile1  = open(filename_of_adjlist_of_trees,'rb')
    adjtree_list = pickle.load(datafile1)
    
    datafile2  = open(filename_of_k_values,'rb')
    k_values_list = pickle.load(datafile2)
       
    solution = []
    print('\n',adjtree_list[6])
    print('\n',k_values_list[6])
    
    for i in range(len(adjtree_list)):  
        labels = Node_labeler(adjtree_list[i],k_values_list[i])
        solution.append(labels)
        print(f'Complete {i}th instance')
    
    ratio = proximity_ratio_list(adjtree_list,solution,k_values_list)
       
    solution_file = open(name_of_solution_file,'wb')
    pickle.dump(solution,solution_file)
    
    
    

#add test case file address in "name_of_source_file" variable below
filename_of_adjlist_of_trees = 'Large_Examples_of_AdjLists_of_Trees'
filename_of_k_values = 'Large_Examples_of_k_values'
#add required solution file address in "name_of_solution_file" variable below
name_of_solution_file = 'Large_example_solutions'

main(filename_of_adjlist_of_trees, filename_of_k_values, name_of_solution_file)
print(f'solution file {name_of_solution_file} generated successfully')