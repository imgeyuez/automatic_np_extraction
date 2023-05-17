# command for parsing
# type 1023_0001416.txt | docker run -i rsennrich/parzu /ParZu/parzu > 1023_0001416_output.txt

# modules to import
import os
import glob
import pandas as pd



# read in all the .txt-files
for filename in glob.glob('*.txt'):
    # one file at a time will be opened and read
    with open(os.path.join(os.getcwd(), filename), 'r', encoding="UTF-8-sig") as file: # open in readonly mode

        # create new filename
        output_filename = str(filename[0:-4]) + "_output.txt"

        # create the command
        command_for_parsing = "type " + filename + " | docker run -i rsennrich/parzu /ParZu/parzu > " + output_filename
        command = 'cmd /c "' +  command_for_parsing + '"'

        # parse the file
        os.system(command)


# create data frames out of the output.txt-files
for filename in glob.glob('*output.txt'):
    # create dataframe with column names
    df = pd.read_csv(filename, sep="\t", header=None)
    df.columns = ["index", "token", "lexem", "?", "POS-Tag", "grammatical info", "refers to", "role", "dunno1", "dunno2"]
    
    # delete columns we do not need
    df = df.drop(["lexem", "?","grammatical info", "dunno1", "dunno2"], axis = 1)
    # go through the dataframe of the file
    for index, row in df.iterrows():
        pass
        # look at the single sentences (as long as index[i] > index[i-1] it is one sentence; as soon as index[i] < index[i-1] a new sentence has started)

        # within that sentence search for the nouns of the sentence

        # look out for any token that is conntected to the noun(s)

        #search for the root of the sentence 

        # extract the nps with the roots of the sentence into a new file

        # finished 
