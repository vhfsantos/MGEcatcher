<p align="center"><img src="img/logo.png" alt="MGEcatcher" width="80%"></p>

**MGEcatcher** is an automated pipeline to identify non-fixed mobile genetic elements (MGE) in a set of long read DNA data.
**MGEcatcher** can be use to remove reads containing those MGEs in order to improve genome assembly, or even to survey transposition events in the giving long read DNA sequencing library. 
**MGEcatcher** only needs to be provided with a fasta file containing the MGE sequences and the long reads fastq file.

# Required softwares

**MGEcatcher** requires:

* R (>=4.0.5)
   * GenomicRanges
   * IRanges
   * ggbio
   * dplyr
* Python3 (>=3.8.3)
   * PyFaidx 
* Bedtools (>=2.30.0)
* Blastn (>=2.9.0)

# Input Data

**MGEcatcher** works with minION or PacBio long reads data in `fastq` format.
Besides the `fastq` file you will also need to input the `fasta` file containing the sequences of the MGEs.

If you don't have this second `fasta`, you can try the following:

1. Download the `gff` annotation file for your reference genome
1. Select only the MGEs features from the raw `gff` (let's call this output `mges-only.gff`)
1. Use `mges-only.gff` as input for the [BEDtools' GetFasta](https://bedtools.readthedocs.io/en/latest/content/tools/getfasta.html) program to extract the sequence of this features.
1. (Optional) You may want to cluster the MGE sequences with tools such as [CD-HIT](http://cd-hit.org/)

Now you can run **MGEcatcher** properlly. 

# Usage

You must run **MGEcatcher** for a single `fastq` file of your library at a time. 
So you may also want to use the `-b` parameter to inform the barcode identifier for the running file.


```sh
MGEcatcher -r reads.fastq -m mges.fasta -o output_name -b Barcode01 -t 10

 -r          fastq file for basecalled reads to be used as subject
 -m          fasta file containing MGE sequences to be used as query
 -o          output filename
 -b          barcode identifier (ex.: BC01)
 -t          number of threads (default: 10)
```

# Output files

**MGEcatcher** outputs several files. Inside the `CLASSIFICATION` folder, you will find the information about the reads containing fixed and non-fixed (_i.e._, optional) MGEs. 
Files named `-readnames.txt` contains only the names of the reads for each classification.
Filed named only `.txt` contains more detailed information about the analysis.

For the `.optionalMGEs.txt` file, the column `queryname` contains the read in which the optional MGE was found. The `seqnames` column contains the names of the reads containing the without-MGE version of the region sequenced by the query.
For the `fixedMGEs.txt`, `queryname` has the name of the reads whose MGE was also find in the read in the `seqnames` column. 

The `.txt` files may be use as input for a transposition analysis of your libraries (_e.g_ for comparing the change in the transposition events among the sequenced libraries). Also, the `.optionalMGEs.txt` file can be use to remove those reads from the raw `fastq` file (_e.g_ for improving the genome assembly of the sequenced libraries). 

# Acknowledgements

This work was founded by Fundação de Amparo à Pesquisa do Estado de São Paulo (FAPESP - Brazil), [grant 2018/25329-9](https://bv.fapesp.br/pt/bolsas/186664/estudo-da-instabilidade-genomica-de-halobacterium-salinarum-nrc-1-via-sequenciamento-de-reads-longas/).
