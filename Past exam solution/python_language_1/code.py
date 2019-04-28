



# import data
import pandas as pd
data = pd.read_csv('python_language_1_data.csv')

# obtain the unique years as keys
years = data['year'].unique()
# create dict with year: rainfall values 
dict_json = {}
for year in years:
    dict_json.update({str(year): list(data['rainfall (mm/day)'][data['year']==year])})
# export dict to json file
import json
with open('result.json', 'w') as fp:
    json.dump(dict_json, fp, indent=4)
    
    
    
def function(file_name, year, line_colour = 'r'):
    
    # import data from filename
    import json
    with open(file_name, 'r') as f:
        file = f.read()
    all_data = json.loads(file)

    # extract data only for specified year
    data = all_data[year]
    
    # plot the daily rainfall for that year
    import numpy as np
    day = np.array(range(len(data)))+1

    # Line plots
    from matplotlib import pyplot as plt
    plt.plot(day, data, c=line_colour)
    plt.savefig("plot.png")

function('result.json', '1998', line_colour = 'r')    
    


from math import sqrt
import numpy as np
def transformation(data):
    return np.array(data) * 1.2 ** sqrt(2)


def apply_transformation_for(data):
    return_list = list()
    for obs in data:
        return_list.append(transformation(obs))
    return return_list

def apply_transformation_compr(data):
    return transformation(data)


import json
with open('result.json', 'r') as f:
    file = f.read()
example = json.loads(file)


d = example['1999']

apply_transformation_for(d)
apply_transformation_compr(d)






def plot_c(file_name, start, end):
    # import data from filename
    import json
    with open(file_name, 'r') as f:
        file = f.read()
    all_data = json.loads(file)
    
    # create data list with years start -> end dates
    dates = np.linspace(start, end, end-start+1, dtype=int)
    
    # mean temp for each year in dates
    mean_temp = list()
    for year in dates:
        mean_temp.append(np.mean(all_data[str(year)]))
    
    # Line plots
    from matplotlib import pyplot as plt
    plt.plot(dates, mean_temp, c='g')
    plt.savefig("plot2.png")

plot_c('result.json', 1988, 2000)




