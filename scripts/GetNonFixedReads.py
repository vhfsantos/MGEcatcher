import os
import argparse

# this function returns a dictionary with keys being the query and subject name
# pasted, separated by "...". The values are the start and end of the 
# alignment, the size and name of the MGE that originated the fragment and the 
# size of the subjected read.

# I constructed this in a way that secondary alignments (i.e., alignments 
# sharing both query and subject names) are appended as a list of dictionaries.

def WriteFeatDic(file):
    FeatDic = dict()
    with open(file, 'r') as blast:
        for line in blast.readlines():
            if line.startswith("#"):
                continue
            row = line.strip().split('\t')
            key = row[0]+"..."+row[1]
            if key not in FeatDic.keys():
                FeatDic[key] = [{'start': row[2],
                                'end': row[3],
                                'MGE-size': (int(row[0].split('_')[1])),
                                'read-size': row[6],
                                'MGE-name': row[0].split('_')[2] }]
            else:
                FeatDic[key].append({'start': row[2],
                                'end': row[3],
                                'MGE-size': (int(row[0].split('_')[1])),
                                'read-size': row[6],
                                'MGE-name': row[0].split('_')[2] })
    return FeatDic

# This function searches for alignments supporting the optional state of the 
# MGEs and writes the name of the subjected read. Note that I added here an 
# important step that remove cases in which the subjected and queried reads are 
# the same. So if a MGE aligned in the read X produced a fragment that aligned 
# on the read X supporting the optional state of this MGE, this will not be 
# considered. We only want cases in which the queried and subjected reads are 
# different. 

def GetOptionalMGEs(FeatDic, barcode, output):
    ReadsToRemove = []
    with open(output+str(barcode)+'.optionalMGEs-readnames.txt','w') as FILEoutRN:
        with open(output+str(barcode)+'.optionalMGEs.txt','w') as FILEout:
            # writting header of plottable file
            FILEout.write('queryname\tseqnames\tstart\tend\tseqlength\tMGE\n')
            for k,v in FeatDic.items():
                # checking if there is only one alignment in this read
                if len(v) == 1:
                    queryREADname = k.split("_")[0]
                    end = int(v[0]['end'])
                    start = int(v[0]['start'])
                    GAPsize = int(start - end)
                    READsize = int(v[0]['read-size'])
                    if (abs(GAPsize) >= 300 * 0.9 
                        and abs(GAPsize) <= 300 * 1.1):
                        READname = k.split('...')[1]
                        # check if subj and query reads are not the same
                        if queryREADname == READname:
                            print('!!! QUERY AND SUBJECT ARE THE SAME, SKIPPING!!!')
                        else:
                            MGEname = v[0]['MGE-name']
                            print('flank of {} in:\n\t{}\nfully mapped in:\n\t{}\n\t({} will be removed)'.format(MGEname,queryREADname, READname, queryREADname))
                            ReadsToRemove.append(queryREADname)
                            # writting file plottable with GRanges
                            FILEout.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(queryREADname, READname,start,end,READsize,MGEname))
                            FILEoutRN.write('{}\n'.format(queryREADname))
    NofReadsToRemove = len(set(ReadsToRemove))
    return(NofReadsToRemove)
                            
def GetFixedMGEs(FeatDic, barcode, output):
    with open(output+str(barcode)+'.fixedMGEs.txt','w') as FILEout:
        with open(output+str(barcode)+'.fixedMGEs-readnames.txt','w') as FILEoutRN:
            # writting header of plottable file
            FILEout.write('queryname\tseqnames\tstart\tend\tseqlength\tMGE\n')
            for k,v in FeatDic.items():
                if len(v) == 2:
                    MGEsize = int(v[0]['MGE-size'])
                    MGEname = v[0]['MGE-name']
                    READname = k.split('...')[1]
                    READsize = int(v[0]['read-size'])
                    startPLOT = v[0]['start']
                    end = int(v[0]['end'])
                    start = int(v[1]['start'])
                    endPLOT = v[1]['end']
                    GAPsize = int(start - end)
                    if (abs(GAPsize) >= MGEsize * 0.9 
                        and abs(GAPsize) <= MGEsize * 1.1):
                        queryREADname = k.split('...')[0].split("_")[0]
                        MGEname = v[0]['MGE-name']
                        # writting file plottable with GRanges
                        # first alignment...
                        FILEout.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(queryREADname, READname,startPLOT,end,READsize,MGEname))
                        # second alignment...
                        FILEout.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(queryREADname, READname,start,endPLOT,READsize,MGEname))
                        FILEoutRN.write('{}\n'.format(queryREADname))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--prefix",
                        type=str, help="prefix for output files", 
                        required = True)
    parser.add_argument("-i","--input", 
                        type=str, help="blast results of 300bp-fragments mapping",
                        required = True)
    parser.add_argument("-o","--output", 
                        type=str, help="output dir to write files",
                        required = True)
    args = parser.parse_args()
    
    output = str(args.output)
    print('== Parsing input')
    FeatDic = WriteFeatDic(args.input)
    print('== Getting reads with optional MGEs')
    NofReadsToRemove = GetOptionalMGEs(FeatDic, args.prefix, output)
    print('=== Wrote {} reads to remove'.format(NofReadsToRemove))
    print('== Getting reads with fixed MGEs')
    GetFixedMGEs(FeatDic, args.prefix, output)
    print('= Done')
    
if __name__ == "__main__":
    main()
