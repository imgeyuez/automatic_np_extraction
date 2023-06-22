# modules to import
import os
import glob
import pandas as pd

collected_nps = list()

# create data frames out of the output.txt-files
for filename in glob.glob('*output.txt'):
        
        # open in readonly mode
        with open(os.path.join(os.getcwd(), filename), 'r', encoding="UTF-8-sig") as file: 

            # d in sentences
            file_input = file.readlines()

            # list to generate a single sentence
            single_sentence = list()

            counter = 0 

            # go through each line/"sentence" of the file
            for line in file_input:
                # if it is not an empty line/"sentence", add it to the 
                # list of a single sentence
                if line[0] != "\n":
                    single_sentence.append(line)

                # empty line/"sentence" indicates the end of a sentence 
                elif line[0] == "\n":
                    # --> clear the list of the single sentence for the new sentence
                    sentence_as_elements = list()
                    
                    # and for every element (row in the file) split the elements and append them as the new sentence
                    for row in single_sentence:
                        elements = row.split("\t")
                        sentence_as_elements.append(elements)
                    
                    #print(sentence_as_elements)
                    #break

                    """
                    --> output until here:
                    the list "sentence_as_elements" where every element is a list which
                    contains the single rows of the file, split by \t
                    [
                    ['1', 'M.', 'M.', 'N', 'NE', 'Fem|_|Sg', '0', 'root', '_', '_\n'], 
                    ['2', 'Meier', 'Meier', 'N', 'NE', 'Fem|_|Sg', '1', 'app', '_', '_\n'], 
                    ['3', 'Müllergasse', 'Müllergasse', 'N', 'NE', 'Fem|_|Sg', '2', 'app', '_', '_\n']
                    ]
                    """

                    # create dataframe with column names
                    df = pd.DataFrame(sentence_as_elements, columns = ["ID", "token", "lemma", "wordtype", "POSTag", "features", "head", "deprel", "dunno1", "dunno2"])
                    
                    # delete columns we do not need
                    df = df.drop(["dunno1", "dunno2"], axis = 1)

                    # print the upper three rows
                    #print(df.head(30))

                    # extract the whole token-column to get the whole sentence 
                    sentence_list = df["token"].values.tolist()
                    #print(sentence_list)

                    token_head_dict = dict()

                    token_id_dict = dict()

                    # generate dictionary 
                    # go through the dataframe of the file
                    for index, row in df.iterrows():
                        token_head_dict[row["token"]] = row["head"]
                        if row["deprel"] == "root":
                            if row["deprel"] == "." or row["deprel"] == ",":
                                 pass 
                            elif row["POSTag"] == "CARD":
                                 pass
                            
                        # add the token and its ID to the other dictionary
                        token_id_dict[row["token"]] = row["ID"]
                        
                    print(token_id_dict)    


                    #print(token_head_dict)

                    # list for all NPs in the sentence
                    all_nps_of_sentence = list()

                    # list for a single NP in the sentence
                    # current_np = list()

                    # go through the dataframe once again
                    for index, row in df.iterrows():

                        # if the wordtype is a noun
                        if row["wordtype"] == "N":

                            # create list for the NP:
                            current_np = list()

                            # get the ID of the noun 
                            id_of_noun = row["ID"]

                            """
                            # # Raha: make a list of the row for the current noun
                            # current_np = list (row['token'])

                            # print(current_np)
                            """

                            # forgot what this was for 
                            current_np.append(row["token"])

                            """
                            #Then we do not need this, so I commented it out.
                            #single_np.append(row["token"])
                            """
                            # check if the any word refers to the noun as head
                            token_head_pairs = token_head_dict.items()

                            for pair in token_head_pairs:
                                
                                # check if the ID of the noun is the deprel of 
                                # another token --> head of the token
                                if id_of_noun in pair[1]:
                                    # get the token
                                    deprel_key = pair[0]
                                    #print(pair, "\n")
                                    current_np.append(pair[0])

                                    #print(current_np)
                    
                                    """
                                    This was already included
                                    #Raha: so I changed it from np to current np:
                                    #current_np.append(pair[0])
                                    """

                                """
                                #Raha: So here we could append the np we found to the np list of the sentence
                                #single_np.append(current_np)

                                -> Yes, but we need to change the variable name
                                as the variable for the goal is already existent
                                """
                            all_nps_of_sentence.append(current_np)
                            #current_np = list()
                            print(all_nps_of_sentence)

                    #break

                    # #Raha: Then, we can append all the nps of all sentences to a collected np list.
                    # #Sorry, if it seems several of embedded lists and then messy! 
                    # #we could think of something better later. It is just tentative.
                    # collected_nps.append(single_np) 

        
        # within that sentence search for the nouns of the sentence

        # look out for any token that is conntected to the noun(s)

        #search for the root of the sentence 

        # extract the nps with the roots of the sentence into a new file

        # finished 
