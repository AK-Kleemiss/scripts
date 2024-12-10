import subprocess
import glob
import os

# Define the directory containing the .gbw files
directory = r"."

# Find all .gbw files in the directory
gbw_files = glob.glob(os.path.join(directory, "*.gbw"))

# Define the executable paths and options (change for your system as necessary)
executable_path = r"E:\QMcalculations\NoSpherA2.exe"
orca_executable_path = r"orca_2aim.exe"
aimqb_executable_path = r"E:\QMcalculations\AIMAll\aimqb.exe"
eli_option = "-eli"
lap_option = "-lap"
resolution_option = "-resolution 0.05" # (change for your purpose as necessary)

# List to hold the subprocesses
processes = []

# Execute the commands for each .gbw file simultaneously
for wfn_file in gbw_files:
    # Remove the .gbw extension for the orca command
    orca_file = os.path.splitext(wfn_file)[0]
    
    # Construct the full commands
    command_eli = f"{executable_path} -wfn {wfn_file} {eli_option} {resolution_option}"
    command_lap = f"{executable_path} -wfn {wfn_file} {lap_option} {resolution_option}"
    command_orca = f"{orca_executable_path} {orca_file}"
    command_aimqb = f"{aimqb_executable_path} -run -maxmem=6000 {orca_file}.wfx"
    
    # Execute the commands
    process_eli = subprocess.Popen(command_eli, shell=True)
    process_lap = subprocess.Popen(command_lap, shell=True)
    process_orca = subprocess.Popen(command_orca, shell=True)
    
    # Append the processes to the list
    processes.append((process_eli, command_eli))
    processes.append((process_lap, command_lap))
    processes.append((process_orca, command_orca))
    
    # Print the commands for verification
    print(f"Executed command: {command_eli}")
    print(f"Executed command: {command_lap}")
    print(f"Executed command: {command_orca}")
    
    # Wait for the orca process to complete before running aimqb
    process_orca.wait()
    
    # Execute the aimqb command
    process_aimqb = subprocess.Popen(command_aimqb, shell=True)
    processes.append((process_aimqb, command_aimqb))
    
    # Print the aimqb command for verification
    print(f"Executed command: {command_aimqb}")

# Wait for all subprocesses to complete and print a Finished message
for process, command in processes:
    process.wait()
    print(f"Finished command: {command}")