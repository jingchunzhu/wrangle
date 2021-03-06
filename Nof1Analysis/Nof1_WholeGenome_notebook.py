# coding: utf-8

# In[ ]:

import sys, string
sys.path.insert(0,"../xena/")
import xenaAPI
import xena_datasetlist

# In[ ]:

import Nof1_functions
Nof1_item = {
    "hub" : "https://itomic.xenahubs.net",
    "dataset" : "latestCCI_EXP_G_TPM_log",
    "mode" : "probe",
    "name" : "itomic_Nof1",
    "label" : "itomic_Nof1",
    "log2Theta" : 0.001,
    "unit": "log(TPM)"
}


# In[ ]:

# get samples
Nof1_sample = raw_input('Enter sample name (e.g. 10-3-B1 or ALL): ') or "ALL"

if Nof1_sample == "ALL":
    Nof1_item["samples"] = xenaAPI.dataset_samples( Nof1_item["hub"], Nof1_item["dataset"])
else:
    if (Nof1_functions.checkSamples (Nof1_sample, Nof1_item["hub"], Nof1_item["dataset"])):
        sys.exit()
    else:
        Nof1_item["samples"]= [Nof1_sample]

print Nof1_item["samples"]


# In[ ]:

# enter gene
genes = raw_input('Enter a single or a list of gene names (e.g. PTEN, AR, or ALL): ') or "ALL"

if Nof1_item["mode"] == "probe":
    if genes =="ALL":
        genes = xenaAPI.dataset_fields( Nof1_item["hub"],  Nof1_item["dataset"])
    else:
        genes = string.split(genes,',')
    genaname_mapping ={}

if len(genes) >10:
    print "genes:", genes[:10],"..."
else:
    print "genes:", genes[:10]


# In[ ]:

# # Enter output file name

outputfile = raw_input('Enter output file name (e.g. ' + Nof1_sample +")") or Nof1_sample
outputfile = "Results_Folder/Whole_Genome/" + outputfile
print "output:", outputfile


# In[ ]:

# comparision list
import xena_datasetlist

comparison_list = [
    xena_datasetlist.TCGA_TNBC_geneExp,
    xena_datasetlist.TCGA_BRCA_tumors_geneExp,
    xena_datasetlist.GTEX_breast_geneExp,
    #xena_datasetlist.TCGA_Breast_Basal_geneExp,
    #xena_datasetlist.TCGA_Breast_Her2_geneExp,
    #xena_datasetlist.TCGA_Breast_LumA_geneExp,
    #xena_datasetlist.TCGA_Breast_LumB_geneExp,
    #xena_datasetlist.TCGA_Breast_Adjacent_Normal_geneExp,
]


# In[ ]:

# ## Run
import itomic_WG_Nof1
for comparison_item in comparison_list:
    itomic_WG_Nof1.itomic_Nof1(Nof1_item, genes, genaname_mapping, comparison_item, outputfile + "_vs_"+ comparison_item["fileLabel"])
print "Done"

