DB=/home/wia/kraken2_db #path to Kraken reference database
THREADS=32

mkdir -p kraken_results #creates a folder to store all the Kraken2 results

for R1 in *_nonhuman.fastq.1.gz
do
  SAMPLE=$(basename "$R1" _nonhuman.fastq.1.gz)0000
  R2="${SAMPLE}_nonhuman.fastq.2.gz"

  echo "Processing ${SAMPLE}"

  kraken2 --db "$DB" --threads $THREADS --paired "$R1" "$R2" --report "kraken_results/${SAMPLE}.report" --output "kraken_results/${SAMPLE}.kraken"

done
