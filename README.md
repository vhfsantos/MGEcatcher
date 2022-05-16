<p align="center"><img src="img/logo.png" alt="MGEcatcher" width="90%"></p>

**MGEcatcher** is an automated pipeline to identify non-fixed mobile genetic elements (MGE) in a set of long read DNA data.
**MGEcatcher** can be used to remove reads containing those MGEs in order to improve genome assembly, or even to survey transposition events in the giving long read DNA sequencing library. 
**MGEcatcher** only needs to be provided with a fasta file containing the MGE sequences and the long reads fastq file.

# Installation

**MGEcatcher** is a Bash script, so it doesn't have to be installed. 
However, it requires the following:

* R (>=4.0.5)
   * GenomicRanges (Bioconductor)
   * IRanges (Bioconductor)
   * ggbio (Bioconductor)
   * dplyr
* Python3 (>=3.8.3)
   * PyFaidx 
* Bedtools (>=2.30.0)
* Blastn (>=2.9.0)
* BBMAP (>=38.96)

If you have [Conda](https://docs.conda.io/en/latest/) in your machine, you can easily install all these tools using the `env.yml` file provided here.

```sh
# clone this repo
git clone https://github.com/vhfsantos/MGEcatcher

# enter the directory
cd MGEcatcher

# create the MGEcatcher environment with all dependencies
conda env create -n MGEcatcher -f misc/env.yml

# activate the MGEcatcher env
conda activate MGEcatcher
```

After, you might want to execute the `MGEcatcher` script to see if the installation was done correctly:

```sh
./MGEcatcher -h
```

# Input Data

**MGEcatcher** works with minION or PacBio long reads data in `fastq` format.
Besides the `fastq` file, you will also need to input the `fasta` file containing the sequences of the MGEs.

If you don't have this MGE seed `fasta` file, you can try the following:

1. Download the `gff` annotation file for your reference genome
1. Select only the MGEs features from the raw `gff` (let's call this output `mges-only.gff`)
1. Use `mges-only.gff` as input for the [BEDtools' GetFasta](https://bedtools.readthedocs.io/en/latest/content/tools/getfasta.html) program to extract the sequence of these features.
1. (Optional) You may want to cluster the MGE sequences with tools such as [CD-HIT](http://cd-hit.org/)

Now you can run **MGEcatcher** properly, passing the created file as the `--mge_seed` parameter. 

# Usage

You must run **MGEcatcher** for a single `fastq` file of your library at a time. 
So you may want to use the `--prefix` parameter to inform the barcode identifier for the output files.


```sh
MGEcatcher --reads <reads.fq> --mge_seed <mge.fa> [--threads <N>] \\
           --output <path/to/output/> --prefix <BC01>

     --reads        Fastq file for basecalled reads to be used as subject
     --mge_seed     Fasta file containing MGE sequences to be used as query
     --output       Output dir name; will be created if does not exist
     --prefix       Prefix for output files (ex.: BC01)
     --threads      Number of threads
```

# Output files

**MGEcatcher** outputs several files. 
Inside the `_classification` folder, you will find the information about the reads containing fixed and unfixed MGEs. 
Files named `-readnames.txt` contains only the names of the reads for each classification.
Filed named only `.txt` contains more detailed information about the analysis.

For the `.unfixedMGEs.txt` file, the column `queryname` contains the read in which the unfixed MGE was found. The `seqnames` column contains the names of the reads containing the without-MGE version of the region sequenced by the query.
For the `fixedMGEs.txt`, `queryname` has the name of the reads whose MGE was also found in the read in the `seqnames` column. 

The `.txt` files may be used as input for a transposition analysis of your libraries (_e.g_ for comparing the change in the transposition events among the sequenced libraries). Also, the `.unfixedMGEs.txt` file can be used to remove those reads from the raw `fastq` file (_e.g_ for improving the genome assembly of the sequenced libraries). 

# Acknowledgements

This work was founded by Fundação de Amparo à Pesquisa do Estado de São Paulo (FAPESP - Brazil), [grant 2018/25329-9](https://bv.fapesp.br/pt/bolsas/186664/estudo-da-instabilidade-genomica-de-halobacterium-salinarum-nrc-1-via-sequenciamento-de-reads-longas/).
