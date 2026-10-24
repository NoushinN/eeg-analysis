a<-commandArgs(trailingOnly=TRUE);out<-if(length(a))a[1] else 'results_R'
x<-read.csv(file.path(out,'regional_bandpower.csv'));y<-read.csv('validation/reference_regional_bandpower.csv')
keys<-c('condition','scenario','region','band')
stopifnot(nrow(x)==nrow(y),!anyDuplicated(x[keys]),!anyDuplicated(y[keys]))
m<-merge(x,y,by=keys,suffixes=c('_R','_Python'));stopifnot(nrow(m)==nrow(x))
for(k in c('power_uV2','relative_pct','retained_epochs','retained_seconds')) {
 a<-m[[paste0(k,'_R')]];b<-m[[paste0(k,'_Python')]]
 stopifnot(all(abs(a-b)<=1e-8*pmax(1,abs(b))))
}
cat('PASS: all regional R outputs match executed Python reference within tolerance.\n')
