import os
import csv
import tkinter.filedialog
import tkinter as tk

root = tk.Tk()
root.withdraw()

print("Select folder containing javadocs files")

input_folder = tk.filedialog.askdirectory()
txt_list = [file for file in os.listdir(input_folder) if file.endswith(".htm")]
txt_list.reverse() # We want to start at the lowest version and work our way up
print(txt_list) # List out all files in the order they'll be processed


javadocfields = {}
for input_file in txt_list:
    path = input_folder

    print(input_file)
    
    infile = open(input_file, 'r')
    fileContents = infile.readlines()
    infile.close


    for line in fileContents:
        if line.startswith("<dt><"): # This is a definded item in the index
            # This mess is just dealing with a bit of drift in how exactly things look over the years by getting rid of it
            itemname = line.partition("<a href=\"")[2].partition("\">")[0]
            version = input_file.strip(".htm") + '/'
            itemname = ''.join(itemname).replace('https://jd.papermc.io/paper/', '').replace(version, '').replace('"', '').split(" ")
            itemname = itemname[0].split('-')
            itemname = itemname[0].split('(')
            # This mess is just dealing with a bit of drift in how exactly things look over the years by getting rid of it
            
            # 1.12.2   -   <dt><span class="memberNameLink"><a href="org/bukkit/Note.Tone.html#A">A</a></span> - org.bukkit.<a href="org/bukkit/Note.Tone.html" title="enum in org.bukkit">Note.Tone</a></dt>
            
            # 1.23.1   -   <dt><a href="https://jd.papermc.io/paper/1.21.3/org/bukkit/Note.Tone.html#A" class="member-name-link">A</a> - Enum constant in enum class org.bukkit.<a href="https://jd.papermc.io/paper/1.21.3/org/bukkit/Note.Tone.html" title="enum class in org.bukkit">Note.Tone</a></dt>
            if input_file.strip(".htm") =="1.21.3": # Define valid things for the current version
                   javadocfields[itemname[0]] = input_file.strip(".htm") #Write to dictionary with the current version number
                   
            if itemname[0] in javadocfields: # Only update existing values, don't add stuff that'd been removed
                javadocfields[itemname[0]] = input_file.strip(".htm") #Write to dictionary with the current version number
            


#print(javadocfields) #See this mess in console

# Write output to CSV file 
with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for key, value in javadocfields.items():
       writer.writerow([key, value])
