Performing the analysis of shotgun metagenomics results from 4 papers to understand the differences in taxonomic abundances of microorganisms in tumor (CRC) samples and in normal samples.

## PAPER DETAILS

Paper 1: Elucidating colorectal cancer-associated bacteria through profiling of minimally perturbed tissue-associated microbiota 

* ENA accession code: PRJNA846495
* Country: Japan
* No. of tumor samples = 11
* No. of normal samples = 0
* Raw reads size: 12 Gb

Paper 2: Colorectal Cancer Archaeome: A Metagenomic Exploration, Tunisia

* ENA accession code: PRJNA905672
* Country: Tunisia
* No. of tumor samples = 35
* No. of normal samples = 33
* Raw reads size: 8 Gb

Paper 3: Multi-omics analysis reveals associations between gut microbiota and host transcriptome in colon cancer patients

* ENA accession code: PRJNA1028158
* Country: China
* No. of tumor samples = 19
* No. of normal samples = 19
* Raw reads size: 88 Gb

Paper 4: The characteristics of tissue microbiota in different anatomical locations and different tissue types of the colorectum in patients with colorectal cancer

* ENA accession code: PRJNA1245618
* Country: China
* No. of tumor samples = 19
* No. of adjacent normal samples = 19
* No. of normal samples = 19
* Raw reads size: 432 Gb

The total patient metadata file used is given in **total_patient_metadata.csv**. 

## DOWNLOADING THE RAW READS

Type the ENA accession codes for each paper separately on the ENA browser. A download link will be present in the data table, which will download an SH file containing the codes to download all the raw reads directly from ENA. Download that SH file and run it on the terminal in the desired folder. 

## QUALITY OF RAW READS

To get the individual sample quality reports of the raw reads, run FastQC on the terminal by typing __fastqc *__ in the folder containing the raw reads. Once the individual quality reports are generated, run MultiQC to aggregate the individual quality reports and produce a summary report for all the reads in the folder. Once the MultiQC report is generated, check the: 

* Sequence quality scores: to get the Phred quality score threshold
* Lengths of sequences: to determine whether the reads are of uniform length
* No. of overrepresented sequences: to assess the amount to be removed later
* Adapter contents: to understand which adapters are present to remove them later

## CLEANING UP OF RAW READS

To clean up the reads, the Trimmomatic tool is used. The raw data contains a lot of unnecessary contents which have to be removed, such as the overrepresented sequences, adapter sequences and the sequences with Phred quality scores of less than 30 (value changes based on preference). The parameters of Trimmomatic are decided based on the MultiQC report of those reads. The FastP tool can also be used to determine which adapters are present in the raw reads. To remove the adapter sequences using Trimmomatic, a reference file containing the adapter sequences is required, which is given as **adapter.fa**. The code to run Trimmomatic is given in **trimmomatic.sh**. The results obtained will be the paired and unpaired files of the forward and reverse reads, out of which only the paired files are required.

## ALIGNMENT OF READS TO HUMAN REFERENCE GENOME

To get only the microbial sequences, the human sequences from the reads should be removed. The first step to do that is to align the reads to the human reference genome, which will split the human and nonhuman reads. Download the latest human reference genome from NCBI: https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000001405.40/  

The tool to be used here is Bowtie2. Create a conda environment for Bowtie2 and install it on that environment. Run Bowtie2 on the paired reads against the human reference genome. The code for Bowtie2 is given in **bowtie2.sh**. The results obtained will be human and nonhuman files, out of which only the nonhuman files are required. It is preferred to separate the human and nonhuman files in different folders.

## METAGENOMIC PROFILING

To get the taxonomic classification, metagenomic profiling needs to be done on the nonhuman files from Bowtie2. The tool to be used here is Kraken2, which requires a Kraken2 database folder to be downloaded, which contains the known sequence databases for bacteria, fungi, archaea, viruses, etc. According to preference, individual databases can be downloaded, or the entire folder can be downloaded. To run Kraken2, use the code given in **kraken2.sh**. The results include 2 files for each sample, a .report file and a .kraken file.

For the PRJNA905672 dataset, Bowtie2 can be performed with the archaea database, or the Kraken pipeline on Galaxy Europe (https://usegalaxy.eu/). To perform the Kraken pipeline on Galaxy Europe, upload the paired reads onto Galaxy, then click on the 'kraken' tool. Select the option for paired reads, and upload the forward (R1) and reverse (R2) reads respectively and in the same order. In the section to select a Kraken database, select 'archaea_2020' and run the tool. To get a combined Kraken report, use the 'Krakentools: Combine multiple Kraken reports' tool and select the Kraken reports generated earlier. Using the combined report, stacked bar plots can be plotted on the terminal.

## COMPUTING TAXONOMIC ABUNDANCE

Using the .report files obtained from Kraken2, we can get the taxonomic abundances of the microbes using the tool Bracken. The code to run Bracken is given in **bracken.sh**. From the results obtained after Bracken is run, stacked bar plots can be made to identify the most abundant species in different samples. 

## PLOTTING STACKED BAR PLOTS FOR TAXONOMIC ABUNDANCE

According to preference, stacked bar plots can be plotted to understand the most abundant species present in the samples. The codes to a few examples are given below: 

* Individual sample-wise: **individual.py**
* All samples combined: **combined.py**
* Male vs. female: **mf.py**
* Tumor vs. normal: **tn.py**

The example results are in the results folder, under the names **individual.png**, **combined.png**, **mf.png**, and **tn.png**. 

Thus, from these graphs, we can understand the difference in microbial species abundance in tumor and normal samples, which can help us identify which species are likely to be related to the progression of CRC.
