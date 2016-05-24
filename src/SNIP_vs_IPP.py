import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


list_of_cols = [0,1,2]
SNIP = pd.read_excel(io="../data/IEEE_SNIP_IPP.xlsx", parse_cols=list_of_cols,header=0)

#jname = "AAC: Augmentative and Alternative Communication"
#selected_journal = SNIP[SNIP["Source Title"]==jname] #make sure it exists!
#selected_journal.drop(selected_journal.columns[[1]], inplace=True, axis=1) # removes Print ISSN
#selected_journal = pd.melt(selected_journal, id_vars='Source Title',var_name="SNIP Year", value_name="Value")
#selected_journal.drop(selected_journal.columns[[0]], inplace=True, axis=1)

#selected_journal.plot()
#plt.legend()
#plt.show()

selected_journal = SNIP
#jnames = []
#for journal in jnames:
#	selected_journal.append( SNIP[SNIP["Source Title"]==journal] )

#selected_journal.drop(selected_journal.columns[[1]], inplace=True, axis=1) # removes Print ISSN
#selected_journal = pd.melt(selected_journal, id_vars='Source Title',var_name="SNIP Year", value_name="Value")
#selected_journal.drop(selected_journal.columns[[0]], inplace=True, axis=1)

print selected_journal

plt.scatter(SNIP["SNIP"],SNIP["IPP"])
plt.legend()
plt.show()





