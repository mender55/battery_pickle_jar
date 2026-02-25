"""
Creator: Mirina Enderlin
consultant: ChatGPT
Date: February 2, 2026
Last Updated: February 24, 2026
Description: This script is for organizing battery cell data into more convenient format for plotting


structure:
- Dictionary:
Battery_name = {
            'metadata':
                 {'procedure': <insert value extracted from sheet>,
                'date_of_test': < " >, 
                'c_rate':<>}, 
            'data': 
                {'cycles': {
                    1:{
                        'steps': <[]>,
                        'voltage':<insert voltage values []>}
                        'step_time':<[]>,
                        'current':<[]>,
                        'total_time':<last time value - initial time value + rest time
                    }
                    2:{
                    }  
                }
            }

"""
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import os
import pickle
import os #allows python to look at folders and files in folders


folder_path = "battery_excels" #user inputs folder name here (include quotation marks and check the folder is in  same directory as this script)
pickle_path = "jar_of_batteries.pkl"     # making the pickle file

if os.path.exists(pickle_path):
    with open(pickle_path, "rb") as f:
        jar_of_batteries = pickle.load(f)
else:
    jar_of_batteries = {}     #the 'mother' dictionary that will hold each individual battery dictionary in pickle file

for filename in os.listdir(folder_path):
    if filename.endswith(".xlsx"): #ensures only excel files are parsed
        excel_path = os.path.join(folder_path, filename) #ensure the correct path to each file
        battery_id = os.path.splitext(filename)[0]
        if battery_id in jar_of_batteries:  #to ensure no duplicates
            print(f"Battery {battery_id} already processed, skipping")
            continue
        print("Processing:", battery_id)


        df = pd.read_excel(excel_path, header=None, nrows = 1) #reads only the first row for extracting metadata

        battery = {'metadata':{},'data':{'cycles':{}}} #creates the empty libraries

        battery['metadata'] = {
            "today_date":    df.iloc[0, 1],
            "test_date":     df.iloc[0, 3],
            "filename":      df.iloc[0, 5],
            "procedure":     df.iloc[0, 7],
            "scap":          df.iloc[0, 10],
            "c_rate":        df.iloc[0, 12],
        }                                   #this is straight from Matthew's code for extracting metadata

        #now redo df to extract numerical data
        df = pd.read_excel(excel_path, header=1)
        df.columns = df.columns.str.strip() #strips excess spaces for calling later
        df = df.dropna(subset=['Cycle P', 'Step']) #drops empty cells, such as footers at end added by software

        for cycle in df['Cycle P'].unique():      #looks only at column with cycle P values
            cycle_df=df[df['Cycle P']==cycle]       #creates a database based on one cycle value at a time
            battery['data']['cycles'][cycle] = {    #INside the cycle dictionary, each parameter is a key and the value is the list of time-series values
                    'step': cycle_df['Step'].tolist(),
                    'test_time': cycle_df['Test Time (Hr)'].tolist(),
                    'voltage': cycle_df['Voltage (V)'].tolist(),
                    'current': cycle_df['Current (mA)'].tolist(),
                    'step_time': cycle_df['Step Time (Hr)'].tolist(),
                    'capacity': cycle_df['Capacity (mAHr)'].tolist(),
                    'energy': cycle_df['Energy (mWHr)'].tolist(), 
                    'mode': cycle_df['MD'].tolist()
                }    #inputs cycle as a key and starts the empty dictionary as a value for each cycle

        #prepping to put all in a pickle file
        jar_of_batteries[battery_id]= battery

with open(pickle_path, 'wb') as f:
    pickle.dump(jar_of_batteries,f)


#thoughts for robustness: what if data is missing a column? what if file is .xls and not xlsx?


#demonstrating data was stored correctly and can be recalled via plotting
plt.figure() #make empty figure

for cycle_number in range(0, 2):   # This allows plotting of a single cycle or multiple cycles at once
    
    all_x = []   #creates empty list of data to be appended based on however many cycles being plotted at once
    all_y = []

    for step in battery['data']['cycles'][cycle_number]['steps']:
        all_x.extend(
            battery['data']['cycles'][cycle_number]['steps'][step]['capacity'] #appends list with cycle data
        )                                                                   #based on parameters input here
        all_y.extend(
            battery['data']['cycles'][cycle_number]['steps'][step]['voltage']
        )

    plt.plot(all_x, all_y, label=f"Cycle {cycle_number}")


plt.xlabel("Capacity (mAh)")    #relabel based on parameters being compared
plt.ylabel("Voltage (V)")
plt.title("Cycle 0: Voltage vs Capacity")
plt.legend()
plt.show()

#make plotting script separate 