Performing the analysis of shotgun metagenomics results from 4 papers to understand the differences in taxonomic abundances of microorganisms in tumor (CRC) samples and in normal samples.

Paper 1: Elucidating colorectal cancer-associated bacteria through profiling of minimally perturbed tissue-associated microbiota 

* ENA accession code: PRJNA846495
* Country: Japan
* No. of tumor samples = 11
* No. of normal samples = 0

Paper 2: Colorectal Cancer Archaeome: A Metagenomic Exploration, Tunisia

* ENA accession code: PRJNA905672
* Country: Tunisia
* No. of tumor samples = 35
* No. of normal samples = 33

Paper 3: Multi-omics analysis reveals associations between gut microbiota and host transcriptome in colon cancer patients

* ENA accession code: PRJNA1028158
* Country: China
* No. of tumor samples = 19
* No. of normal samples = 19

Paper 4: The characteristics of tissue microbiota in different anatomical locations and different tissue types of the colorectum in patients with colorectal cancer

* ENA accession code: PRJNA1245618
* Country: China
* No. of tumor samples = 19
* No. of adjacent normal samples = 19
* No. of normal samples = 19

The total patient metadata file used is given in **metadata.csv**. 

## DOWNLOADING THE RAW READS

Type the ENA accession codes for each paper separately on the ENA browser. A download link will be present in the data table, which will download an SH file containing the codes to download all the raw reads directly from ENA. Download that SH file and run it on the terminal in the desired folder. 

## QUALITY OF RAW READS

To get the individual sample quality reports of the raw reads, run FastQC on the terminal by typing __fastqc *__ in the folder containing the raw reads. Once the individual quality reports are generated, run MultiQC to aggregate the individual quality reports and produce a summary report for all the reads in the folder. Once the MultiQC report is generated, check the: 

* Sequence quality scores: to get the Phred quality score threshold
* Lengths of sequences: to determine whether the reads are of uniform length
* No. of overrepresented sequences: to assess the amount to be removed later
* Adapter contents: to understand which adapters are present to remove them later

## CLEANING UP OF RAW READS

To clean up the reads, the Trimmomatic tool is used. The raw data contains a lot of unnecessary contents which have to be removed, such as the overrepresented sequences, adapter sequences and the sequences with Phred quality scores of less than 30 (value changes based on preference). The parameters of Trimmomatic are decided based on the MultiQC report of those reads. The FastP tool can also be used to determine which adapters are present in the raw reads. To remove the adapter sequences using Trimmomatic, a reference file containing the adapter sequences is required, which is given as **adapter.fa**. The code to run Trimmomatic is given in **trimmomatic.sh**.

## ALIGNMENT OF READS TO HUMAN REFERENCE GENOME
