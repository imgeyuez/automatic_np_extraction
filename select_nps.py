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

# list for the selected nps
selected_nps = list()

# create data frames out of the output.txt-files
for filename in glob.glob('*output.txt'):

    # read in the file
    with open(os.path.join(os.getcwd(), filename), 'r', encoding="UTF-8-sig") as file: # open in readonly mode
        file_input = file.readlines()
        # generate a sentence
        single_sentence = list()
        for line in file_input:
            if line[0] != "\n":
                single_sentence.append(line)
            elif line[0] == "\n":
                sentence_into_elements = list()
                for row in single_sentence:
                    elements = row.split("\t")
                    sentence_into_elements.append(elements)
                
                # generate dataframe
                df = pd.DataFrame(sentence_into_elements, columns = ["index", "token", "lexem", "?", "POS-Tag", "grammatical info", "refers to", "role", "dunno1", "dunno2"])
                # delete columns we do not need
                df = df.drop(["lexem", "?","grammatical info", "dunno1", "dunno2"], axis = 1)
                #print(df)

                
                # search for the needed POS-tag and their connection and create a pair of them to add to the list of pairs
                for ind, row in df.iterrows():
                    # within that sentence search for the nouns of the sentence
                    if row["POS-Tag"] == "N": #because PPOSAT refers to his, her, our, my, your, and their
                        pass
                        # continuation
                        
                        # look out for any token that is conntected to the noun(s)

                        #search for the root of the sentence 

                        # extract the nps with the roots of the sentence into a new file

                        # finished 
                    
                # clear the list
                single_sentence = list()
