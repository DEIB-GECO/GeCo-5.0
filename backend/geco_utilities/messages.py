gecoagent = "I am GecoAgent, your assistant through the extraction, the analysis and the visualization of genomic data. Let's proceed with the analysis."
mood = "I am good thank you! Let's proceed with the analysis."
initial_greeting = "Hi, there!"
start_init = "What data are you looking for?"
healthy_patients = "Do you want healthy patients?"
wrong_choice = "Sorry, your choice is not available. Please reinsert one."
filter_more = "Do you want to filter more? If so, which one do you want to select now?"
confirm_selection = "You can see your choices in the bottom right panel.\nDo you want to keep your selection?"
restart_selection = "Do you want to restart the selection from scratch?"
download = "You can download the data by clicking on the arrow in the bottom panel."
choice_field = "Which field do you want to select?"
change_field = "Which field do you want to change?"
wrong_field = "The field is not valid, please select another one"
assign_name = "Do you want to assign a name to your dataset? If so provide a name."
rename = "You can define the name to give to the dataset that you have extracted. From now on, that name will be used."
metadata_filter = "You can also select samples with specific conditions. Do you want to filter on metadata?"
metadatum_choice = "Which metadatum do you want to filter on?\n You can see your choices in the right pane."
metadatum_value = "Which value do you want to select?\nIf you want more, please separate them using ';'."
metadatum_range = "Which range of values do you want? You can tell me the minimum or maximum value or both.\nThe values are shown in the histogram."
other_metadatum = "Please choose another key."
chosen_values = "Ok, the chosen values are shown in the bottom right pane."
other_metadata = "Do you want to filter on other metadata?"
other_dataset = "Do you want to select another dataset?"
no_metadata_range = "There aren't available data for the requested values."
bye_message = "Ok, thank you! Bye!"
gmql_operations = 'Do you want to modify the extracted data?'
gmql_unary= 'Which operation do you want to do?'
gmql_binary= 'How do you want to put together the two selected datasets?'
no_ann_found = "I could not find any annotation file with the filters you selected. Please insert one by one."
no_exp_found = "I could not find any data with the filters you selected. Please insert one by one."
start_binary = 'Do you want to put together the two extracted datasets? If so, which operation do you want to perform?'
pivot_message = "Now I will put the data in a table, so as you can analyze them easily."
row_meta_message = "You have to define what to put in the rows. Which metadatum do you want?"
row_region_message = "You have to define what to put in the rows. Which region do you want?"
column_meta_message = "You have to define what to put in the column. Which metadatum do you want?"
column_region_message = "You have to define what to put in the columns. Which region do you want?"
value_region_message = "With region data do you want to use to fill your table?"
not_understood = "Sorry, I didn't understand your choice. Can you repeat?"
cover_message = "To do the cover, I will ask you the minimum and the maximum accumulation values, then if you want you can insert a metadatum on which group the output dataset.\nLet's start from the minimum accumulation value."
modify_metadata = "We are beginning a Project operation, to create a new metadatum or modifying an existing one.\n" \
                  " Write the name of an existing metadatum, if you want to modify its values, or tell me a new name for the metadatum you want to create."
modify_region = "We are beginning a Project operation, to create a new region datum or modifying an existing one. Write the name of an existing region datum, if you want to modify its values, or a brand new name for the region datum you want to create."
#modify_region = "With the project, you can modify a region datum or select a list of region data to keep and discard the others.\nDo you want to modify a region datum? If so, which one?"
#modify_metadata = "With the project, you can modify a metadatum or select a list of metadata to keep and discard the others.\nDo you want to modify a metadatum? If so, which one?"
meta_region_to_modify = "You are going to modify {}."
meta_to_add = "You are creating {} metadatum."
region_to_add = "You are creating {} as new region."
project_meta3 = "If you want to assign the same value for all the samples just digit it (e.g., 3, true, \"my label\").\nIf you want to compute its value starting from an existing metadatum, please tell me the metadatum name."
project_region3 = "If you want to assign the same value for all the samples just digit it (e.g., 3, true, \"my label\").\nIf you want to compute its value starting from an existing region, please tell me the region name."
cover_not_understood = 'Sorry I didn\'t understand, choose a number or write any'
choose_max = 'Now please choose the maximum threshold for the overlapping regions.'
groupby = 'Do you want to group by one or more metadata? If not, the entire dataset will be collapsed in a single sample.'
groupby_values = 'Instead, if you want the groupby, insert the metadata, if more than one separate them using \';\''
new_gmql_operation = 'Do you want to do another operation on this dataset?'
arithmetic_operation = 'Which operation do you want to do?'
want_arithmetic = 'Do you want to do an arithmetic operation?'
sum_meta = 'Please, insert the value or the metadatum you want to add'
sub_meta = 'Please, insert the value or the metadatum you want to subtract'
prod_meta = 'Please, insert the factor.\nIt can be either a value or a metadatum.'
div_meta=  'Please, insert the divider\nIt can be either a value or a metadatum.'
rename_meta = 'Do you want to rename the metadatum?\nIf so, provide a name'
keep = 'Ok.\nPlease, tell me which ones you want.\nIf you want more, please separate them using ';'.'
sum_region = 'Please, insert the value or the region datum you want to add'
sub_region = 'Please, insert the value or the region datum you want to subtract'
prod_region = 'Please, insert the factor.\nIt can be either a value or a region datum.'
div_region=  'Please, insert the divider\nIt can be either a value or a region datum.'
rename_region = 'Do you want to rename the region datum?\nIf so, provide a name'
joinby = "Do you want to add a metadatum for the joinby?\nIf so, which one?"
union = "Ok. I will do the union of the two datasets"
difference = "Ok. I will do the difference of the two datasets"
aggregate_fun = "Which aggregate function do you want?"
named = "OK, dataset saved with name: {}"