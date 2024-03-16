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
paraview_path = r'C:\Program Files\ParaView 5.11.0\bin\paraview.exe'    # Useful for debugging
paraview_path = r'C:\Program Files\ParaView 5.11.0\bin\pvbatch.exe'
macro_directory = current_directory + r'\Macros'

# Check if the ParaView executable exists
if not os.path.exists(paraview_path):
    print("ParaView executable not found at the specified path.")
    exit()

# Check if the macro directory exists
if not os.path.exists(macro_directory):
    print("Macro directory not found at the specified path.")
    exit()

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
    print('################################################################')
    print("Available Macros:")
    for i, macro_file in enumerate(macro_files, start=1):
        color = Fore.RED + Style.BRIGHT if macro_file in executed_macros else ''
        print(f"{color}{i}. {macro_file}")

# Initial display
display_macros()

# Add an option for exiting the script
print("0. Exit")

while True:
    # Prompt the user for input
    selected_macro_number = int(input("Enter the number of the macro you want to run, or 0 to exit: "))

    # 0 closes the script
    if selected_macro_number == 0:
        exit()

    if 1 <= selected_macro_number <= len(macro_files):
        # Get the selected macro file
        selected_macro = os.path.join(macro_directory, macro_files[selected_macro_number - 1])

        # Use subprocess to run ParaView with the --script option
        subprocess.run([paraview_path, selected_macro])

        # Confermation
        print(Fore.YELLOW + macro_files[selected_macro_number - 1] + ' has run successfully\n' + Style.RESET_ALL)

        # Add the executed macro to the list
        executed_macros.append(os.path.basename(selected_macro))

        # Display available macros with updated colors
        display_macros()
