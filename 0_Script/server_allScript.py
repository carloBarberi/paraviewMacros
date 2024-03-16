import os
import subprocess
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Get the directory of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Change the current working directory to the script directory
os.chdir(script_directory)

# Get current directory
current_directory = os.getcwd()

# Specify the paths
paraview_path = r'C:\Program Files\ParaView 5.11.0\bin\pvbatch.exe'
macro_directory = current_directory + r'\Macros'

# Check if the ParaView executable exists
if not os.path.exists(paraview_path):
    print("ParaView executable not found at the specified path.")
    exit()

# Check if the macro directory exists
if not os.path.exists(macro_directory):
    print("Macro directory not found at the specified path.")
    #exit()

# Get a list of all macro files in the directory
macro_files = [f for f in os.listdir(macro_directory) if f.endswith('.py')]

# Check if there are any macro files
if not macro_files:
    print("No macro files found in the specified directory.")
    exit()

# List to store executed macros
executed_macros = []

# Function to display available macros with color
def display_macros():
    for i, macro_file in enumerate(macro_files, start=1):
        color = Fore.RED + Style.BRIGHT if macro_file in executed_macros else ''
        print(f"{color}{i}. {macro_file}")

# Initial display
print('######################################################')
print("Macros will run in the following order:")
display_macros()

# It is useful to stop the script from running
print()
user = input("Type 1 to continue or 0 to exit: ")
print()

# Loop to run all the macros
if  user == '1':
    for i, macro_file in enumerate(macro_files, start=1):
        # Get the selected macro file
        selected_macro = os.path.join(macro_directory, macro_file)

        # Use subprocess to run ParaView with the --script option
        subprocess.run([paraview_path, selected_macro])

        # Confermation
        print(Fore.YELLOW + macro_file + ' has run successfully\n' + Style.RESET_ALL)

        # Add the executed macro to the list
        executed_macros.append(os.path.basename(selected_macro))

    # Display available macros with updated colors
    print('######################################################')
    display_macros()

    # Wait for user to press ENTER before exiting
    input("Press ENTER to exit. ")
else:
    exit()