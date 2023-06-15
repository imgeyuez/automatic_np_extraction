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

                    #Raha
                    collected_nps = []

                    np = list()

                    for index, row in df.iterrows():
                         if row["Wordtype"] == "N":
                            index_of_noun = row["index"]

                            # Raha: make a list of the row for the current noun
                            current_np = list (row['token'])

                            # check if the any word referes to the noun
                            key_value_pairs = token_refers_to_dict.items()
                            
                            #Then we do not need this, so I commented it out.
                            #np.append(row["token"])

                            for pair in key_value_pairs:

                                if index_of_noun in pair[1]:
                                    # get the token
                                    deprel_key = pair[0]
                                    print(pair, "\n")
                                    
                                    #Raha: so I changed it from np to current np:
                                    current_np.append(pair[0])
                            
                            #Raha: So here we could append the np we found to the np list of the sentence
                            np.append(current_np)

                    #Raha: Then, we can append all the nps of all sentences to a collected np list.
                    #Sorry, if it seems several of embedded lists and then messy! 
                    #we could think of something better later. It is just tentative.
                    collected_nps.append(np) 

                    print(collected_nps)
                        # continuation
                        
                        # look out for any token that is conntected to the noun(s)

                        #search for the root of the sentence 

                        # extract the nps with the roots of the sentence into a new file

                        # finished 
                    
                # clear the list
