# command for parsing
# type 1023_0001416.txt | docker run -i rsennrich/parzu /ParZu/parzu > 1023_0001416_output.txt

# modules to import
import os
import glob
import pandas as pd


"""
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
"""
collected_nps = list()

# create data frames out of the output.txt-files
for filename in glob.glob('*output.txt'):
        with open(os.path.join(os.getcwd(), filename), 'r', encoding="UTF-8-sig") as file: # open in readonly mode
            # extract sentences
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

                    # create dataframe with column names
                    df = pd.DataFrame(sentence_into_elements, columns = ["index", "token", "lexem", "Wordtype", "POSTag", "grammatical info", "deprel", "role", "dunno1", "dunno2"])
                    
                    # delete columns we do not need
                    df = df.drop(["lexem","grammatical info", "dunno1", "dunno2"], axis = 1)

                    # print the upper three rows
                    print(df.head(30))

                    token_refers_to_dict = dict()

                    # go through the dataframe of the file
                    for index, row in df.iterrows():
                        token_refers_to_dict[row["token"]] = row["deprel"]

                    print(token_refers_to_dict)

                    np = list()

                    for index, row in df.iterrows():
                         if row["Wordtype"] == "N":
                            index_of_noun = row["index"]
                            # check if the any word referes to the noun
                            key_value_pairs = token_refers_to_dict.items()
                            np.append(row["token"])
                            for pair in key_value_pairs:

                                if index_of_noun in pair[1]:
                                    # get the token
                                    deprel_key = pair[0]
                                    print(pair, "\n")
                                    np.append(pair[0])
                                    
                    print(np)
                        # continuation
                        
                        # look out for any token that is conntected to the noun(s)

                        #search for the root of the sentence 

                        # extract the nps with the roots of the sentence into a new file

                        # finished 
                    
                # clear the list
