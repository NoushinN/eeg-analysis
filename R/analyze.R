# Base R only. Run from repository root: Rscript R/analyze.R data/anonymized results
args <- commandArgs(trailingOnly=TRUE)
input <- if(length(args)>0) args[1] else 'data/anonymized'
out <- if(length(args)>1) args[2] else 'results'
dir.create(out, recursive=TRUE, showWarnings=FALSE)
read_edf <- function(path) {
 con <- file(path,'rb'); on.exit(close(con))
 txt <- function(n) trimws(readChar(con,n,useBytes=TRUE))
 version<-txt(8); patient<-txt(80); recording<-txt(80); date<-txt(8); time<-txt(8)
 hb<-as.integer(txt(8)); reserved<-txt(44); nr<-as.integer(txt(8)); dur<-as.numeric(txt(8)); ns<-as.integer(txt(4))
 stopifnot(version=='0',nr>0,!grepl('EDF\\+D',reserved))
 widths<-c(label=16,transducer=80,unit=8,pmin=8,pmax=8,dmin=8,dmax=8,prefilter=80,samples=8,reserved=32)
 h<-lapply(widths,function(w) replicate(ns,txt(w)))
 for(k in c('pmin','pmax','dmin','dmax','samples')) h[[k]]<-as.numeric(h[[k]])
 stopifnot(hb==256+256*ns,file.info(path)$size==hb+nr*sum(h$samples)*2)
 x<-lapply(h$samples,function(n) numeric(n*nr))
 for(r in seq_len(nr)) for(j in seq_len(ns)) x[[j]][((r-1)*h$samples[j]+1):(r*h$samples[j])]<-readBin(con,'integer',h$samples[j],size=2,signed=TRUE,endian='little')
 keep<-which(h$label!='EDF Annotations')
 stopifnot(all(h$unit[keep]=='uV'),length(unique(h$samples[keep]))==1)
 x<-sapply(keep,function(j) (x[[j]]-h$dmin[j])*(h$pmax[j]-h$pmin[j])/(h$dmax[j]-h$dmin[j])+h$pmin[j])
 colnames(x)<-sub('-CPz$','',h$label[keep]);list(x=x,fs=h$samples[keep[1]]/dur,duration=nr*dur)
}
# One-sided, periodic-Hann modified periodogram; constant detrending only.
periodogram <- function(x,fs) {
 n<-nrow(x); w<-0.5-0.5*cos(2*pi*(0:(n-1))/n)
 z<-mvfft(sweep(x,2,colMeans(x))*w)
 p<-Mod(z[1:(n/2+1),,drop=FALSE])^2/(fs*sum(w*w))
 p[2:(n/2),]<-2*p[2:(n/2),];p
}
bands<-list(delta=c(1,4),theta=c(4,8),alpha=c(8,13),beta=c(13,30))
files<-c(EO='recording_1_EO.edf',EC='recording_3_EC.edf',TCF='recording_4_Intervention.edf')
raw<-lapply(files,function(f) read_edf(file.path(input,f)))
excluded<-c('F3','T8','M1','M2') # F3/T8 quality; mastoids excluded from scalp summary
roi<-c('P3','Pz','P4','P7','P8','O1','Oz','O2')
quality<-data.frame(); epochs<-data.frame(); summaries<-data.frame(); spectra<-data.frame(); inventory<-data.frame()
for(cond in names(raw)) {
 d<-raw[[cond]];x<-d$x;fs<-d$fs;n<-as.integer(4*fs);stopifnot(n%%2==0)
 inventory<-rbind(inventory,data.frame(condition=cond,duration_s=d$duration,fs_hz=fs,signal_channels=ncol(x)))
 for(ch in colnames(x)) {
  xx<-matrix(x[seq_len(floor(nrow(x)/n)*n),ch],nrow=n)
  quality<-rbind(quality,data.frame(condition=cond,channel=ch,median_sd_uV=median(apply(xx,2,sd)),median_ptp_uV=median(apply(xx,2,function(v)diff(range(v)))),fraction_ptp_gt150=mean(apply(xx,2,function(v)diff(range(v)))>150)))
 }
 for(scenario in c('primary','strict100','matched280','all_available')) {
  limit<-if(scenario=='matched280')280 else d$duration
  threshold<-if(scenario=='strict100')100 else 150
  starts<-seq(0,floor(limit/4)*4-4,by=4)
  # Remove first and last complete epoch to reduce transition/export-boundary contamination.
  if(scenario!='all_available') starts<-starts[-c(1,length(starts))]
  chans<-setdiff(colnames(x),excluded); f<-(0:(n/2))*fs/n
  ps<-list(); pr<-list()
  for(t in starts) {
   z<-x[(t*fs+1):((t+4)*fs),chans,drop=FALSE]
   ptp<-apply(z,2,function(v)diff(range(v))); flat<-apply(z,2,sd)<0.1
   jump<-apply(z,2,function(v)max(abs(diff(v))))>50
   good<-ptp<=threshold & !flat & !jump
   keep_global<-all(good);keep_roi<-all(good[match(roi,chans)])
   p<-periodogram(z,fs)
   epochs<-rbind(epochs,data.frame(condition=cond,scenario=scenario,start_s=t,keep_global=keep_global,keep_posterior=keep_roi,n_bad_channels=sum(!good),max_ptp_uV=max(ptp)))
   if(keep_global) ps[[length(ps)+1]]<-p
   if(keep_roi) pr[[length(pr)+1]]<-p[,match(roi,chans),drop=FALSE]
  }
  for(region in c('scalp','posterior')) {
   pp<-if(region=='scalp')ps else pr;cc<-if(region=='scalp')chans else roi
   if(!length(pp))next
   avg<-Reduce('+',pp)/length(pp)
   for(j in seq_along(cc)) for(band in names(bands)) {
    ix<-f>=bands[[band]][1]&f<bands[[band]][2]; total<-sum(avg[f>=1&f<30,j])*fs/n
    val<-sum(avg[ix,j])*fs/n
    summaries<-rbind(summaries,data.frame(condition=cond,scenario=scenario,region=region,channel=cc[j],band=band,power_uV2=val,relative_pct=100*val/total,retained_epochs=length(pp),retained_seconds=4*length(pp)))
   }
   if(scenario=='primary') spectra<-rbind(spectra,data.frame(condition=cond,region=region,frequency_hz=f,psd_uV2_Hz=rowMeans(avg)))
  }
 }
}
write.csv(inventory,file.path(out,'recordings.csv'),row.names=FALSE)
write.csv(quality,file.path(out,'channel_quality.csv'),row.names=FALSE)
write.csv(epochs,file.path(out,'epoch_quality.csv'),row.names=FALSE)
write.csv(summaries,file.path(out,'channel_bandpower.csv'),row.names=FALSE)
write.csv(spectra,file.path(out,'spectra.csv'),row.names=FALSE)
agg<-aggregate(cbind(power_uV2,relative_pct,retained_epochs,retained_seconds)~condition+scenario+region+band,summaries,mean)
write.csv(agg,file.path(out,'regional_bandpower.csv'),row.names=FALSE)
contrasts<-data.frame()
for(sc in unique(agg$scenario))for(reg in unique(agg$region))for(b in names(bands))for(pair in list(c('TCF','EC'),c('EC','EO'))) {
 a<-subset(agg,scenario==sc&region==reg&band==b&condition==pair[1]);z<-subset(agg,scenario==sc&region==reg&band==b&condition==pair[2])
 if(nrow(a)*nrow(z)==1)contrasts<-rbind(contrasts,data.frame(scenario=sc,region=reg,band=b,contrast=paste(pair,collapse='_vs_'),change_pct=100*(a$power_uV2/z$power_uV2-1),change_dB=10*log10(a$power_uV2/z$power_uV2),relative_change_pp=a$relative_pct-z$relative_pct))
}
write.csv(contrasts,file.path(out,'contrasts.csv'),row.names=FALSE)
png(file.path(out,'spectra_R.png'),width=1400,height=700,res=140);par(mfrow=c(1,2))
for(reg in c('scalp','posterior')) {
 s<-subset(spectra,region==reg&frequency_hz>=1&frequency_hz<=30)
 plot(NA,xlim=c(1,30),ylim=range(10*log10(s$psd_uV2_Hz)),xlab='Frequency (Hz)',ylab='PSD (dB relative to 1 uV^2/Hz)',main=reg)
 for(i in seq_along(files)){a<-subset(s,condition==names(files)[i]);lines(a$frequency_hz,10*log10(a$psd_uV2_Hz),col=i,lwd=2)}
 legend('topright',names(files),col=1:3,lty=1,bty='n')
};dev.off()
capture.output(sessionInfo(),file=file.path(out,'R_sessionInfo.txt'))
