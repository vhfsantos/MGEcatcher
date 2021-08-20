<p align="center"><img src="img/logo.png" alt="MGEcatcher" width="90%"></p>

**MGEcatcher** is an automated pipeline to identify non-fixed mobile genetic elements (MGE) in a set of long read DNA data.
It can be used to remove reads containing those MGEs in order to improve genome assembly, or even to survey transposition events in the giving long read library. **MGEcatcher** only needs to be provided with a fasta file containing the MGE sequences and the long reads fastq file.

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

# Acknowledgements

This work was founded by Fundação de Amparo à Pesquisa do Estado de São Paulo (FAPESP - Brazil), (grant 2018/25329-9)[https://bv.fapesp.br/pt/bolsas/186664/estudo-da-instabilidade-genomica-de-halobacterium-salinarum-nrc-1-via-sequenciamento-de-reads-longas/].
