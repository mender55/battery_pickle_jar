'''
Creator: Mirina Enderlin
consultant: ChatGPT
Date: February 24, 2026
Last Updated: February 24, 2026
'''
import pandas as pd
import matplotlib.pyplot as plt
import os
import pickle

pickle_path = "jar_of_batteries.pkl" #input pickle file with all the battery data to plot

if os.path.exists(pickle_path):
    with open(pickle_path, "rb") as f:
        jar_of_batteries = pickle.load(f)

    print(jar_of_batteries.keys())  #in case one forgets the EXACT name of battery as logged in pickle file
    input("Press Enter to continue...") 

    battery_to_plot = "1014_MC" #user inputs battery name here (include quotation marks and check the battery is in the pickle file)
    #demonstrating data was stored correctly and can be recalled via plotting
    
    if battery_to_plot not in jar_of_batteries:
        raise ValueError(f"{battery_to_plot} not found in pickle file.")

    # 🔥 THIS WAS MISSING
    battery = jar_of_batteries[battery_to_plot]

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
