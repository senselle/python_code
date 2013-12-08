#!/usr/bin/python
import sys
import os


#ssh s_elle@195.70.204.3

#dobi2014
step = []
def pipeline(SRR, app):
  name=os.path.basename(SRR[:-4])
  step.append('wget %s' % SRR)
  step.append('fastq-dump --split-files %s' % os.path.basename(SRR))
  step.append('/home/akomissarov/libs/FastQC/fastqc -t 30 -o /home/bioinf/public/results/sc %s%s %s%s' % (name, "-1.fastq", name, "-2.fastq"))
  step.append('java -jar /home/akomissarov/libs/Trimmomatic-0.30/trimmomatic-0.30.jar PE -phred33 %s%s %s%s %s%s %s%s %s%s %s%s %s' \
            % (name, "-1.fastq", name, "-2.fastq", name, "_1_paired.fq.gz", name, "_1_unpaired.fq.gz", name, "_2_paired.fq.gz", name, "_2_unpaired.fq.gz", \
             "ILLUMINACLIP:/home/akomissarov/libs/Trimmomatic-0.30/adapters/TruSeq3-PE.fa:2:30:10 TRAILING:20 MINLEN:36"))
  step.append('/home/akomissarov/libs/FastQC/fastqc -t 30 -o /home/bioinf/public/results/sc %s%s %s%s' % (name, "-1.fastq", name, "-2.fastq"))
  step.append('gunzip %s%s' % (name, "_1_unpaired.fq.gz"))
  step.append('gunzip %s%s' % (name, "_2_unpaired.fq.gz"))
  step.append('cat %s%s %s%s %s %s%s' % (name, "_1_unpaired.fq", name, "_1_unpaired.fq", ">", name, "_unpaired_merged.fastq"))
  step.append('/home/akomissarov/libs/FastQC/fastqc -t 30 -o /home/bioinf/public/results/sc %s%s' % (name, "_unpaired_merged.fastq"))
  if app == "tophat":
     step.append('tophat -o %s%s %s %s%s %s%s %s%s' % (name, ".sam", "/home/s_elle/bt2_S288C/bt2_S288C", name, "_1_paired.fq.gz", name, "_2_paired.fq.gz", name,"_unpaired_merged.fastq"))
  elif app == "bowtie2":
    step.append('bowtie2 -D %s%s %s %s%s %s%s %s%s' % (name, ".sam", "/home/s_elle/bt2_S288C/bt2_S288C", name, "_1_paired.fq.gz", name, "_2_paired.fq.gz", name, "_unpaired_merged.fastq"))
  else:
    exit(1)
     
  #for i in step: 
   #os.system(i)
   #print i
  os.system("time " + " && ".join(step))
   

if  __name__ == '__main__':
#pipeline(sys.argv[1], sys.argv[2])

  pipeline("ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR453/SRR453569/SRR453569.sra", "tophat")
