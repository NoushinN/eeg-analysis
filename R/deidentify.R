# Creates header-redacted copies; never overwrites the original files.
# The supplied files' annotations were manually checked and contain task labels only.
# This function does NOT sanitize arbitrary EDF+ free-text annotations.
args<-commandArgs(trailingOnly=TRUE)
if(length(args)!=2)stop('Usage: Rscript R/deidentify.R ORIGINAL_DIR OUTPUT_DIR')
dir.create(args[2],recursive=TRUE,showWarnings=FALSE)
for(n in c('recording_1_EO.edf','recording_3_EC.edf','recording_4_Intervention.edf')) {
 src<-normalizePath(file.path(args[1],n));dst<-file.path(args[2],n)
 if(normalizePath(dirname(dst))==dirname(src))stop('Output must differ from original directory')
 b<-readBin(src,'raw',n=file.info(src)$size)
 field<-function(text,n)charToRaw(sprintf(paste0('%-',n,'s'),text))
 b[9:88]<-field('X X X X',80)
 b[89:168]<-field('Startdate 01-JAN-2000 X X X',80)
 b[169:176]<-charToRaw('01.01.00');b[177:184]<-charToRaw('00.00.00')
 writeBin(b,dst)
}
