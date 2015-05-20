import string, os, sys
import json,datetime

PATHPATTERN= "CopyNumber_Gistic2"
LEVEL="Level_4"

import TCGAUtil
sys.path.insert(0,"../CGDataNew")
from CGDataUtil import *

tmpDir = "tmpTry/"

def CopyNumber_Gistic2 (inDir, outDir, cancer,flog,REALRUN):
    if string.find(string.upper(cancer),"PANCAN")!=-1:
        return
    if string.find(string.upper(cancer),"KIPAN")!=-1:
        return
    if string.find(string.upper(cancer),"GBMLGG")!=-1:
        return
    if string.find(string.upper(cancer),"STES")!=-1:
        return
        
    garbage=[tmpDir]
    if os.path.exists( tmpDir ):
        os.system("rm -rf "+tmpDir+"*")
    else:
        os.system("mkdir "+tmpDir)

    #figure out the FH date
    if inDir[-1]!="/":
        s = inDir+"/"
    else:
        s=inDir
    FHdate = string.split(s,"/")[-2]

    #single file in dir mode, uncompress to dir
    dataDir =""
    lastDate=""
    for file in os.listdir(inDir):
        #find the file
        if string.find(file,PATHPATTERN)!=-1 and string.find(file,LEVEL)!=-1 and string.find(file,"md5")==-1:
            pass
        else:
            continue

        if not os.path.exists(inDir +file+".md5"):
            print "file has no matching .md5 throw out", file
            continue        

        #file date
        lastDate=  datetime.date.fromtimestamp(os.stat(inDir+file).st_mtime)
        
        #is tar.gz?, uncompress
        if string.find(file,".tar.gz")!=-1:
            if REALRUN:
                os.system("tar -xzf "+inDir+file +" -C "+ tmpDir) 
                dataDir = tmpDir +os.listdir(tmpDir)[0]+"/"
            print file
            break

    #make sure there is data
    if REALRUN and (dataDir =="" or (not os.path.exists(dataDir))):
#    if dataDir =="" or (REALRUN and not os.path.exists(dataDir)):
        cleanGarbage(garbage)
        return

    #print status
    print cancer, __name__
    
    #set output dir
    if not os.path.exists( outDir ):\
        os.makedirs( outDir )
    if not os.path.exists( outDir +cancer+"/"):
        os.makedirs( outDir+cancer+"/" )

    #data processing single dir mode
    #for pattern in ["all_data_by_genes","all_thresholded.by_genes","focal_data_by_genes"]:
    for pattern in ["all_data_by_genes","all_thresholded.by_genes"]:
        cgFileName= "Gistic2_"+PATHPATTERN
        cgFileName = cgFileName +"_"+pattern

        if REALRUN:
            file =""
            for file in os.listdir(dataDir):
                if string.find(file,pattern)!=-1:
                    break
            if REALRUN and file!="":
                command= "cut -f 1,4- "+dataDir+file+" > "+outDir+cancer+"/"+cgFileName
                os.system(command)
            
        if not os.path.exists(outDir+cancer+"/"+cgFileName):
            continue

        oHandle = open(outDir+cancer+"/"+cgFileName+".json","w")
        J={}
        #stable
        if pattern=="all_data_by_genes":
            suffix="gistic2"
            namesuffix="gistic2"
            
        if pattern=="all_thresholded.by_genes":
            suffix="gistic2_thresholded"
            namesuffix="gistic2thd"
        
        J["cgDataVersion"]=1
        J["label"]= "copy number ("+suffix+")"
        J["longTitle"]="TCGA "+TCGAUtil.cancerOfficial[cancer]+" ("+cancer+") copy number "+suffix+" estimate"
        J["dataSubType"]="copy number (gene-level)"
        J["redistribution"]= True
        J["groupTitle"]="TCGA "+TCGAUtil.cancerGroupTitle[cancer]
        J["dataProducer"]= "TCGA FIREHOSE pipeline"        
        J["url"]= "http://gdac.broadinstitute.org/runs/analyses__"+FHdate[0:4]+"_"+FHdate[4:6]+"_"+FHdate[6:8]+"/data/"+cancer+"/"+FHdate[0:8]+"/"
        J["version"]= datetime.date.today().isoformat()
        J["wrangler"]= "cgData TCGAscript "+ __name__ +" processed on "+ datetime.date.today().isoformat()
                
        J["anatomical_origin"]= TCGAUtil.anatomical_origin[cancer]
        J["sample_type"]=["tumor"]
        J["primary_disease"]=TCGAUtil.cancerGroupTitle[cancer]
        J["cohort"] ="TCGA "+TCGAUtil.cancerHumanReadable[cancer]
        J['domain']="TCGA"
        J['tags']=["cancer"]+ TCGAUtil.tags[cancer]
        J['owner']="TCGA"
        
        #change description
        J["wrangling_procedure"]= "FIREHOSE data download from TCGA DCC, processed at UCSC into cgData repository"
                
        if pattern=="all_data_by_genes":
            J["description"]= "TCGA "+ TCGAUtil.cancerOfficial[cancer]+" ("+cancer+")"\
                              " gene-level copy number variation (CNV) estimated using the GISTIC2 method.<br><br>"+ \
                              " Copy number profile was measured experimentally using whole genome microarray at a TCGA genome characterization center. Subsequently, TCGA FIREHOSE pipeline applied GISTIC2 method to produce segmented CNV data, which was then mapped to genes to produce gene-level estimates."+\
                              " Genes are mapped onto the human genome coordinates using UCSC cgData HUGO probeMap."+\
                              " Reference to GISTIC2 method PMID:21527027."


        if pattern=="all_thresholded.by_genes":
            J["description"]= "TCGA "+ TCGAUtil.cancerOfficial[cancer]+" ("+cancer+")"\
                              " thresholded gene-level copy number variation (CNV) estimated using the GISTIC2 method.<br><br>"+ \
                              " Copy number profile was measured experimentally using whole genome microarray at a TCGA genome characterization center. Subsequently, GISTIC2 method was applied using the TCGA FIREHOSE pipeline to produce gene-level copy number estimates. GISTIC2 further thresholded the estimated values to -2,-1,0,1,2, representing homozygous deletion, single copy deletion, diploid normal copy, low-level copy number amplification, or high-level copy number amplification."+\
                              " Genes are mapped onto the human genome coordinates using UCSC cgData HUGO probeMap."+\
                              " Reference to GISTIC2 method PMID:21527027."
        """    
        if pattern=="focal_data_by_genes":
            J["description"]= "TCGA "+ TCGAUtil.cancerOfficial[cancer]+" ("+cancer+")"\
                              " gene-level focal copy number variation (CNV) estimated using the GISTIC2 method.<br><br>"+ \
                              " Copy number profile was measured experimentally using whole genome microarray at a TCGA genome characterization center. Subsequently, GISTIC2 method was applied using the TCGA FIREHOSE pipeline to produce focal gene-level copy number estimates. GISTIC2 separates CNV profiles into underlying arm-level and focal alterations (short CNV segments that map to small regions of the genome) based on CNV segment length. FIREHOSE further maps segmented CNV data to genes. This dataset shows only the gene-level focal CNV events."+\
                              " Genes were mapped onto the human genome coordinates using UCSC cgData HUGO probeMap."+\
                              " Reference to GISTIC2 method PMID:21527027."
        """                      
        J["description"] = J["description"] +"<br><br>"
                
        #change cgData
        J["name"]="TCGA_"+cancer+"_"+namesuffix
        name = trackName_fix(J['name'])
        if name ==False:
            message = "bad object name, need fix otherwise break loader, too long "+J["name"]
            print message
            flog.write(message+"\n")
            return
        else:
            J["name"]=name        
            
        J[":probeMap"]= "hugo"
        J["type"]= "genomicMatrix" 
        J[":sampleMap"]="TCGA."+cancer+".sampleMap" 
                
        oHandle.write( json.dumps( J, indent=-1 ) )
        oHandle.close()

    cleanGarbage(garbage)
    return

def cleanGarbage(garbageDirs):
    for dir in garbageDirs:
        os.system("rm -rf "+ dir+"*")
    return

