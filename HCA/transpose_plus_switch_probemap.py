import string, sys, os
import csv
from itertools import izip
import uuid

probeMap = ""

def parse(probeMap):
    probeID_gene_mapping = {}
    fin = open(probeMap, 'r')
    fin.readline()
    for line in fin.readlines():
        data = line[:-1].split('\t')
        probe = data[0]
        gene = data[1]
        probeID_gene_mapping[probe] = gene
    fin.close()
    return probeID_gene_mapping

def process (infile, outfile, input_delimiter, probeID_gene_mapping):
    fout=open(outfile,'w')
    fout.close()
    fout=open(outfile,'a')

    #header
    fin=open(infile,'rU')
    line = fin.readline()
    totalN = len(string.split(line, input_delimiter))
    fin.close()

    k = 200
    count = 0
    tmpFile = str(uuid.uuid4())
    os.system("mkdir " + tmpFile)
    for i in range (0, totalN, k):
        count = count + 1
        tmpinfile = tmpFile + "/." + str(count)
        start = i + 1 #linux cut
        command = "cut -f " + str(start) + "-" + str(start+k-1) +" " + infile + " > " + tmpinfile
        os.system(command)

        fin=open(tmpinfile,'rU')
        a = izip(*csv.reader(fin, delimiter = input_delimiter))
        fin.close()

        #switch gene ids in a
        for row in a:
            probeID = row[0]
            gene = probeID_gene_mapping[probeID]
            row[0] = gene
        csv.writer(fout, delimiter="\t", lineterminator="\n").writerows(a)
        os.system("rm -rf " + tmpinfile)

    fout.close()
    os.system("rm -rf " + tmpFile)

if len(sys.argv[:])!= 5:
    print "python transpose.py fin fout input_delimiter(e.g.\"\\t\") size(e.g.200 larger the file, smaller the size)"
    sys.exit()

infile = sys.argv[1]
outfile= sys.argv[2]
input_delimiter = sys.argv[3]
k = sys.argv[4]

probeID_gene_mapping = parse(probeMap)
process(infile, outfile, input_delimiter, probeID_gene_mapping)

