import argparse
from pyfaidx import Fasta

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("-u","--upstream", type=str, help="upstream fasta file", required = True)
	parser.add_argument("-d","--downstream", type=str, help="downstream fasta file", required = True)
	parser.add_argument("-o","--output", type=str, help="output fasta name", required = True)

	args = parser.parse_args()
# 0018b243-bf93-4e55-b35c-08c6b18a9e8f_1398_ISH3B::NC_002607.1:95825-97223::0018b243-bf93-4e55-b35c-08c6b18a9e8f:7792-7942
	with Fasta(args.upstream) as upstream,\
		Fasta(args.downstream) as downstream, \
		open(args.output,'w') as result:
		for a,b in zip(upstream, downstream):
		        #MGEstart = a.name.split(":")[1].split("-")[1]
		        #print(MGEstart)
		        #MGEend = b.name.split(":")[1].split("-")[0]
		        #print(MGEend)
		        #readName = a.name.split(":")[0]
		        #print(readName)
		        #header = readName+":"+MGEstart+":"+MGEend
		        header = a.name.split("::")[0]
		        result.write('>' + header)
		        result.write('\n'+str(a))
		        result.write(str(b)+'\n')

if __name__ == "__main__":
    main()
