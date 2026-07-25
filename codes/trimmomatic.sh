THREADS=32
TRIMMOMATIC=/home/wia/softwares/miniconda3/share/trimmomatic/trimmomatic.jar #path to the trimmomatic.jar file
ADAPTER=/data/mohan_metagenomics/crc_tissue_samples/PRJNA284355/adapter.fa #path to the adapter.fa file 

for R1 in *_1.fastq.gz
do
  SAMPLE=${R1%_1.fastq.gz}
  R2=${SAMPLE}_2.fastq.gz
  
  java -jar $TRIMMOMATIC PE \
    -threads $THREADS \
    -phred33 \
    $R1 $R2 \
    $[SAMPLE]_R1_paired.fastq.gz \
    ${SAMPLE}_R1_unpaired.fastq.gz \ 
    $[SAMPLE]_R2_paired.fastq.gz \
    ${SAMPLE}_R2_unpaired.fastq.gz \
    ILLUMINACLIP: adapter.fa:2:30:10 \
    LEADING: 30 \ #how many bp to trim from the front
    TRAILING: 30 \ #how many bp to remove from the back
    SLIDINGWINDOW: 4:30 \ #the number of bp to read and check at a time : the Phred quality score threshold
    MINLEN: 100 #minimum length of the sequence

done
I
