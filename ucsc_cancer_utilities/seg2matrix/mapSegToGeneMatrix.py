#!/usr/bin/env python

import sys,string,copy
import CGData.RefGene
import CGData.GeneMap
import segToProbeMap

if __name__ == "__main__":
    if len(sys.argv[:])!=5:
        print "python mapSegToGeneMatrix.py genomicsSegmentIn refGene GeneLevelMatrixOut NORMAL_CNV\n"
        sys.exit()
    refgene = CGData.RefGene.RefGene()
    refgene.load( sys.argv[2] )

    NORMAL_CNV=sys.argv[4]

    #* b for cnv
    probeMapper = CGData.GeneMap.ProbeMapper('b')

    fin =open(sys.argv[1],'r')
    genes= {}
    samples={}
    matrix=[]  #sample then gene
    matrix_weight =[]
    for gene in refgene.get_gene_list():
        genes[gene]=len(genes)

    Ngene = len(genes.keys())
    oneSample=[]
    for i in range(0, Ngene):
        oneSample.append('');

    print "genes: ", len(genes)

    count =0

    while 1:
        count = count+1
        line =fin.readline()
        #print line, count
        if line =="": # end of file
            break
        if count ==1:
            continue #ignore the first line
        line = string.strip(line)
        if line == "": # empty line
            continue
        if line[0]=="#":
            continue
        tmp = string.split(line,"\t")
        if len(tmp)!= 5:
            continue
        seg = segToProbeMap.probeseg("", tmp[1], int(tmp[2]), int(tmp[3]),".")
        sample = tmp[0]
        value = float(tmp[4])

        if sample not in samples:
            samples[sample]=len(samples)
            matrix.append(copy.deepcopy(oneSample))
            matrix_weight.append(copy.deepcopy(oneSample))

        hits={}
        for hit in probeMapper.find_overlap( seg, refgene ):
            gene = hit.name
            if gene in hits:
                continue
            hits[gene]=0
            gene_length = hit.chrom_end - hit.chrom_start + 1
            overlap_start = max(int(tmp[2]), hit.chrom_start)
            overlap_end =  min(int(tmp[3]), hit.chrom_end)
            overlap_length = overlap_end - overlap_start + 1
            weight = overlap_length / float(gene_length)

            if matrix[samples[sample]][genes[gene]] == '':
                matrix[samples[sample]][genes[gene]] = 0.0
                matrix_weight[samples[sample]][genes[gene]] = 0.0
            matrix[samples[sample]][genes[gene]] =+ value * weight
            matrix_weight[samples[sample]][genes[gene]] =+ weight

            #print int(tmp[2]), int(tmp[3]), hit.chrom_start, hit.chrom_end, gene_length, overlap_length, weight
    fin.close()

    print "segments: ", count

    fout =open(sys.argv[3],'w')
    sample_list =samples.keys()
    fout.write("sample\t"+string.join(sample_list,"\t")+"\n")
    print genes["MYC"]
    for gene in genes.keys():
        fout.write(gene)
        for sample in sample_list:
            total = matrix[samples[sample]][genes[gene]]
            if total == '':
                average = NORMAL_CNV
            else:
                total=matrix[samples[sample]][genes[gene]]
                t_weight =matrix_weight[samples[sample]][genes[gene]]
                average = total / t_weight
                average =round(average,6)
            fout.write("\t"+str(average))
        fout.write("\n")
    fout.close()
