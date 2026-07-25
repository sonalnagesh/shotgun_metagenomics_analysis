INDEX=/data/mohan metagenomics/crc_tissue_samples/GRCh38.p14_hg/ncbI_dataset/data/GCA_000001405.29/GRCh38 #path to human reference genome files
THREADS=32

mkdir -p host_separated #creates a folder to store all the outputs from Bowtie2

for R1 in *_R1_paired.fastq.gz
do
  SAMPLE=${R1%_R1_paired.fastq.gz}
  R2="${SAMPLE}_R2_paired.fastq.gz"

  echo "Processing ${SAMPLE}"

  bowtie2 -p ${THREADS} -x ${INDEX} -1 "$R1" -2 "$R2" --very-sensitive --un-conc-gz host_separated/${SAMPLE}_nonhuman.fastq.gz --al-conc-gz host_separated/${SAMPLE}_human.fastq.gz -S host_separated/${SAMPLE}.sam 2> host_separated/${SAMPLE}.log

done
