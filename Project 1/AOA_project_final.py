import pickle
#go at last to add test case file address/name for running
def Multiline_parameters(x,y):
    
    points_len = len(x)    
    error_matrix = [[0]*points_len for j in range(points_len)]
    for i in range(points_len - 2):
        error_matrix[i][i], error_matrix[i][i+1] = 0,0
        sigma_x = [x[i], x[i]+x[i+1]]
        sigma_y = [y[i], y[i]+y[i+1]]
        sigma_x2 = [x[i]**2, x[i]**2 + x[i+1]**2]
        sigma_y2 = [y[i]**2, y[i]**2 + y[i+1]**2]
        sigma_xy = [x[i]*y[i], x[i]*y[i] + x[i+1]*y[i+1]]

        for j in range(i+2, points_len):
            n = j-i+1
            x_values =  x[j] + sigma_x[j-i-1] 
            y_values =  y[j] + sigma_y[j-i-1] 
            x2_values =  x[j]*x[j] + sigma_x2[j-i-1] 
            y2_values =  y[j]*y[j] + sigma_y2[j-i-1] 
            xy_values =  x[j]*y[j] + sigma_xy[j-i-1]
            sigma_x.append(x_values)
            sigma_y.append(y_values)
            sigma_x2.append(x2_values)
            sigma_y2.append(y2_values)
            sigma_xy.append(xy_values)

            a = ((n*xy_values) - (x_values*y_values))/((n*x2_values) - (x_values**2))
            b = (y_values - a*x_values)/n
            error_matrix[i][j] = y2_values + a*a*x2_values + n*b*b + 2*a*b*x_values - 2*a*xy_values - 2*b*y_values
   
    return error_matrix
 
def Multiline_fitting(x,y,c):
   
    error_matrix  = Multiline_parameters(x,y)
    n = len(error_matrix[0])
    optimal_cost = [0]*n
    line_si_ind = [0]*n
    
    for j in range(n):
        optimal_temp = [0]*(j+1)
        optimal_temp[0] = error_matrix[0][j] + c
        
        for i in range(1,j+1):
            optimal_temp[i] = optimal_cost[i-1] + error_matrix[i][j] + c
        
          
        min_value = min(optimal_temp)
        optimal_cost[j] = min_value
        line_si_ind[j] = optimal_temp.index(min_value)
  
    line_ei_ind = []
    j = n-1
    while j >= 0:
        line_ei_ind.append(j)
        j = int(line_si_ind[j]-1)

    line_ei_ind.reverse()
    return line_ei_ind, optimal_cost[-1]  

def main(name_of_source_file, name_of_solution_file):
    
    datafile  = open(name_of_source_file,'rb')
    data = pickle.load(datafile)

    instances = len(data['n_list'])
    solution = {}
    solution['k_list'] = []
    solution['last_points_list'] = []
    solution['OPT_list'] = []
   
    for i in range(instances):
        x = data['x_list'][i]
        y = data['y_list'][i]
        c = data['C_list'][i]
        last_points, opt = Multiline_fitting(x,y,c)
        solution['k_list'].append(len(last_points))
        solution['last_points_list'].append(last_points)
        solution['OPT_list'].append(opt)
        print(f'Complete {i}th instance')
    
    solution_file = open(name_of_solution_file,'ab')
    pickle.dump(solution,solution_file)
    

#add test case file address in "name_of_source_file" variable below
name_of_source_file = 'examples_of_large_instances'
#add required solution file address in "name_of_solution_file" variable below
name_of_solution_file = 'examples_of_large_instances_solution999'    
main(name_of_source_file, name_of_solution_file)
print(f'solution file {name_of_solution_file} generated successfully')
        
    

