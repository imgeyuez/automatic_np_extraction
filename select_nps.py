# modules to import
import os
import glob
import pandas as pd
import pickle 

# create new folder for the files
# folder_name = "data_with_selected_nps"
# folder = os.path.join("c:/Users/imgey/Desktop/UNI_MASTER_RUB/SoSe23/Korpuslinguistische Analysen der Nominalflexion im Deutschen/automatische NP extraction", folder_name)


# go through the files in the folder
for filename in glob.glob('*output.txt'):

    # list to store ALL nps of ONE FILE in
    nps_of_file = list()

    sentence_counter = 1
    np_counter = 1

    # open the file in read-mode
    with open(os.path.join(os.getcwd(), filename), 'r', encoding="UTF-8-sig") as file: 

        # read in the lines of token
        file_input = file.readlines()

        # list to generate a single sentences out of the file
        single_sentence = list()
        

        # go through each line/"sentence" of the file
        for line in file_input:
            # if it is not an empty line/"sentence", add it to the 
            # list of a single sentence
            if line[0] != "\n":
                single_sentence.append(line)

            # empty line/"sentence" indicates the end of a sentence 
            elif line[0] == "\n":
                # split each element of the sentence into the single token-information
                sentence_as_elements = list()
                for row in single_sentence:
                    elements = row.split("\t")
                    sentence_as_elements.append(elements)
                
                # create dataframe with column names
                df = pd.DataFrame(sentence_as_elements, columns = ["ID", "token", "lemma", "wordtype", "POSTag", "features", "head", "deprel", "dunno1", "dunno2"])
                
                # delete columns we do not need
                df = df.drop(["dunno1", "dunno2"], axis = 1)

                # extract the whole token-column to get the whole sentence as tokens
                sentence_list = df["token"].values.tolist()
                sentence_as_string = " ".join(sentence_list)
                number_of_tokens_of_sentence = len(sentence_list)

                token_head_list = list()

                token_index_list = list()

                token_id_list = list()

                # generate dictionary 
                # go through the dataframe of the file
                for index, row in df.iterrows():
                    token_head_list.append([[row["token"]], row["head"]])

                    
                    # find the root 
                    if row["deprel"] == "root":
                        if str(row["deprel"]).isalpha() == True:

                            root_of_sentence = df.loc[index, :].values.flatten().tolist()
                        else:
                            if root_of_sentence:
                                root_of_sentence == "None"
                            else:
                                pass
                                                        
                    # add the token and its index to the other dictionary
                    token_index_list.append([[row["token"]], index])
                    token_id_list.append([[row["token"]], row["ID"]])

                # list for all NPs in the sentence
                all_nps_of_sentence = list()

                # go through the dataframe once again
                for index, row in df.iterrows():

                    # if the wordtype is a noun
                    if row["wordtype"] == "N":

                        # create list for the NP:
                        current_np_ids = list()

                        # get all the info of the noun 
                        info_of_noun = df.loc[index, :].values.flatten().tolist()

                        id_of_noun = info_of_noun[0]
                        head_of_noun_ID = info_of_noun[6]

                        # append the nouns ID to the list
                        current_np_ids.append(id_of_noun)

                        if int(head_of_noun_ID) != 0:
                            current_np_ids.append(head_of_noun_ID)

                        # in the following:
                        # check if any word refers to the noun as head
                        for ind, token_head_pair in enumerate(token_head_list):
                            
                            # check if the ID of the noun is the deprel of 
                            # another token --> noun is head of that token
                            if id_of_noun == token_head_pair[1]:
                                
                                # append the ID of the token of the sentence 
                                # --> get a list with IDs, can sort them and 
                                # then create a second list with the filled in token (information)
                                current_np_ids.append(token_id_list[ind][1])

                        current_np_ids.sort()
                        number_of_tokens_of_np = len(current_np_ids)

                        # create NP with the regarding token information, based on the IDs
                        current_np = list()

                        for token_id in current_np_ids:
                            index_in_df = int(token_id) - 1
                            if int(index_in_df) < 0:
                                token_info = tuple(df.loc[int(token_id), :].values.flatten().tolist())
                            else:
                                token_info = tuple(df.loc[int(index_in_df), :].values.flatten().tolist())

                            current_np.append(token_info)

                        """
                        create the final form of the single np on form of:
                        [	Satz_NP-Nummer,
                            Dateiname {str},
                            Satz_ID_NR {int},
                            Satz {str}, 
                            (root, POS-Tag, grammatical_info) {tuple},
                            Anzahl-der-Token-der-NP {int},
                            [NP] {list}, Bsp.: [(token1, POS-tag, grammatical_info),... (token-n, POS-tag, grammatical_info)],
                        ]
                        """

                        sentence_np_id = str(sentence_counter) + "_" + str(np_counter)

                        final_form_of_np = [sentence_np_id, filename, sentence_counter, sentence_as_string, root_of_sentence, number_of_tokens_of_np, current_np]

                        np_counter += 1

                        all_nps_of_sentence.append(final_form_of_np)

                # --> clear the list of the single sentence for the new sentence
                single_sentence = list()

                sentence_counter += 1      
                nps_of_file.append(all_nps_of_sentence)  

                # print(nps_of_file)
                nps_of_file.append("\n")

    filename_2_0 = filename.replace(".txt", "")

    newfilename = str(filename_2_0) + str("_exported_nps.txt")

    # print the final list into a new txt-file for the other groups to 
    # process further 
    with open(newfilename, "a", encoding="UTF-8-sig") as f:
        print(nps_of_file, file=f)
