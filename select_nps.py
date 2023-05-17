import os
import glob

# daten einlesen

# every .txt-file in the folder ...
for filename in glob.glob('*.txt'):
    # ... will be opened and read
    with open(os.path.join(os.getcwd(), filename), 'r', encoding="UTF-8-sig") as file: # open in readonly mode
        #os.system('cmd /c "Your Command Prompt Command"')
        output_filename = str(filename[0:-4]) + "_output.txt"
        command_for_parsing = "type " + filename + " | docker run -i rsennrich/parzu /ParZu/parzu > " + output_filename
        command = 'cmd /c "' +  command_for_parsing + '"'
        print(command)
        os.system(command)
        
# datein in ein pandas frame umwandeln

# aus dem pandas frame daten löschen, die wir nicht benötigen

# aus den übrigen die Nomen heraussuchen

# connections zu den Nomen heraussuchen

# roots herausfiltern

# fertig ? :D
