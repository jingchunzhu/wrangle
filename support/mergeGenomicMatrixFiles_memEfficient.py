import sys,string,os
import json,datetime
import math
import copy
import uuid

def merge (infile_list, outfile):
    genes={}
    allgenes={}
    files=[]
    tmpDir =str(uuid.uuid4())

    os.system("mkdir "+ tmpDir)

    for infile in infile_list:
        if not os.path.exists(infile):
            print infile, "not exists"
            sys.exit()
        genes = setGeneOrder (infile,genes)
    allgenes = posToGene(genes)

    for infile in infile_list:
        nCOLs = getColumnSize (infile)
        cur_genes={}
        cur_genes = setGeneOrder (infile,cur_genes)

        for i in range (2,nCOLs, 250):
            tmpfile = tmpDir+"/tmp_"+str(int(i/250.0))
            os.system("cut -f "+ i+"-"+i+249+" "+infile +" > tmp")
            process(cur_genes, "tmp", allgenes, tmpfile)
            files.append(tmpfile)

    #paste all together
    os.system("paste -d \'\' "+string.join(files," ")+" > "+ outfile)

    return

def posToGene(genes):
    allGenes ={}
    for gene in genes:
        p = genes[gene]
        allGenes[p]=gene

def setGeneOrder (infile,genes):
    os.system("cut -f 1 "+infile +" > tmpid")
    fin=open("tmpid",'U')    
    fin.readline()
    for line in fin.readlines():
        hugo = line[:-1]
        if hugo not in genes:
            p=len(genes)
            genes[hugo]=p
    fin.close()
    return genes

def getColumnSize (infile):
    fin=open(infile,'U')    
    fin.readline()
    fin.close()
    return len(string.split(line[:-1],"\t"))

def process(cur_genes, infile, allgenes, outfile):
    fin=open(infile,'U')    
    fout=open(infile,'w') 

    line = fin.readline()
    fout.write(line)

    nCOL = len(string.split(line,'\t'))
    emptyList =[]
    for i in range(0,nCOL):
        emptyList.append("")
    emptyLine =string.join(emptyList,'\t')+"\n"

    lines = fin.readlines()
    for i in range(0,len(allgenes)):
        gene = allgenes[i]
        if gene in cur_genes:
            p = cur_genes[gene]
            fout.write(lines[p])
        else:
            fout.write(emptyLine)
    fin.close()
    fout.close()
    return 

if len(sys.argv[:])<3:
    print "python mergeGenomicMatrixFiles_memEfficient.py outfile infiles"
    sys.exit()

outfile = sys.argv[1]
infile_list =sys.argv[2:]
merge (infile_list, outfile)
