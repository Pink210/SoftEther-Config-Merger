import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import os

# Global variables to store file paths
config_file_path1 = ""
config_file_path2 = ""
output_folder = ""

def read_config(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def extract_users(config):
    start = config.find('declare UserList')
    if start == -1:
        return None  # Handle case when 'declare UserList' is not found
    
    open_braces = 0
    end = start
    for i, char in enumerate(config[start:]):
        if char == '{':
            open_braces += 1
        elif char == '}':
            open_braces -= 1
            if open_braces == 0:
                end = start + i + 1
                break
    
    return config[start:end-6]

def merge_configs(config1, config2):
    users1 = extract_users(config1)
    users2 = extract_users(config2)
    
    with open('user_set1.config', 'w') as file:
        file.write(users1)
    with open('user_set2.config', 'w') as file:
        file.write(users2)
    # Handle case when either config doesn't contain 'declare UserList'
    if not users1:
        return config2
    if not users2:
        return config1
    
    # Split the user blocks and create a set to avoid duplicates
    user_set1 = set(users1.split('\n					declare ')[1:])
    user_set2 = set(users2.split('\n					declare ')[1:])
    
    # Remove any users from user_set2 that are already in user_set1
    user_set2.difference_update(user_set1)
    
    # Combine the user lists
    combined_users = '\n'.join('\n					declare ' + user for user in user_set2)
    
    # Insert the combined user list back into config1
    insert_point = config1.find('declare UserList')
    end_point = config1.find('\n				}', insert_point) + 1
    return config1[:end_point] + '\n' + combined_users + '\n' + config1[end_point:]

def browse_file1():
    global config_file_path1
    config_file_path1 = filedialog.askopenfilename()
    if config_file_path1:
        browse_button1.config(text=f"Browse File 1: {config_file_path1}")

def browse_file2():
    global config_file_path2
    config_file_path2 = filedialog.askopenfilename()
    if config_file_path2:
        browse_button2.config(text=f"Browse File 2: {config_file_path2}")

def clear_files():
    global config_file_path1, config_file_path2
    config_file_path1 = ""
    config_file_path2 = ""
    browse_button1.config(text="Browse File 1")
    browse_button2.config(text="Browse File 2")

def convert_configs():
    global config_file_path1, config_file_path2, output_folder
    if config_file_path1 == "" or config_file_path2 == "":
        messagebox.showerror("Error", "Please select both config files.")
        return
    filename = filedialog.asksaveasfilename(defaultextension=".config", filetypes=[("Config files", "*.config")])
    if filename:
        config1 = read_config(config_file_path1)
        config2 = read_config(config_file_path2)
        merged_config = merge_configs(config1, config2)
        with open(filename, 'w') as file:
            file.write(merged_config)
        output_folder = os.path.dirname(filename)
        messagebox.showinfo("Success", "Merge completed successfully.")
        browse_button_output.config(state=tk.NORMAL)

def browse_output_folder():
    if output_folder:
        os.startfile(output_folder)

# Create the GUI
root = tk.Tk()
root.title("Config Merger")
root.geometry("500x200")  # Set the window size

# Create style for themed widgets
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 10))

# Create buttons without icons
browse_button1 = ttk.Button(root, text="Browse File 1", command=browse_file1)
browse_button1.pack(pady=5)

browse_button2 = ttk.Button(root, text="Browse File 2", command=browse_file2)
browse_button2.pack(pady=5)

convert_button = ttk.Button(root, text="Merge", command=convert_configs)
convert_button.pack(pady=5)

clear_button = ttk.Button(root, text="Clear Files", command=clear_files)
clear_button.pack(pady=5)

browse_button_output = ttk.Button(root, text="Browse Output Folder", command=browse_output_folder, state=tk.DISABLED)
browse_button_output.pack(pady=5)

root.mainloop()

