<p align="center"><img src="img/logo.png" alt="MGEcatcher" width="90%"></p>

**MGEcatcher** is an automated pipeline to identify non-fixed mobile genetic elements (MGE) in a set of long read DNA data. It requires a fasta file with MGE sequences and the long reads fastq file. 

# Requirements

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
