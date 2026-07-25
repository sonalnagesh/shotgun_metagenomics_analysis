DB=/home/wia/kraken2_db #path to Kraken reference database
THREADS=32

for report in *.report
do
  SAMPLE=$(basename "$report" .report)
  
  echo "Processing ${SAMPLE}"

  bracken -d "$DB" -i "$report" -o "${SAMPLE}.bracken.species" -r 150 -l S # -r is the average length of all the reads and -l determines the level of classification where S means species and G means genus

done
