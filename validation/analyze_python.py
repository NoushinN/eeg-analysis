"""Independent implementation of R/analyze.R; also generates review figures."""
from pathlib import Path
import sys, csv, json
import numpy as np
import scipy
from scipy.signal import periodogram
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[1]
source=Path(sys.argv[1]) if len(sys.argv)>1 else root/'data/anonymized'
out=Path(sys.argv[2]) if len(sys.argv)>2 else root/'results'
out.mkdir(parents=True,exist_ok=True)
files={'EO':'recording_1_EO.edf','EC':'recording_3_EC.edf','TCF':'recording_4_Intervention.edf'}
bands={'delta':(1,4),'theta':(4,8),'alpha':(8,13),'beta':(13,30)}
roi=['P3','Pz','P4','P7','P8','O1','Oz','O2']
def read_edf(path):
 b=path.read_bytes(); ns=int(b[252:256]);nr=int(b[236:244]);dur=float(b[244:252]);off=256;h={}
 assert b[:8].strip()==b'0' and b'EDF+D' not in b[192:236] and nr>0
 for k,n in [('label',16),('transducer',80),('unit',8),('pmin',8),('pmax',8),('dmin',8),('dmax',8),('prefilter',80),('samples',8),('reserved',32)]:
  h[k]=[b[off+i*n:off+(i+1)*n].decode().strip() for i in range(ns)];off+=ns*n
 for k in ['pmin','pmax','dmin','dmax','samples']: h[k]=np.array(h[k],float)
 assert len(b)==off+nr*int(sum(h['samples']))*2
 data=[[] for _ in range(ns)];annotations=[]
 for r in range(nr):
  for j in range(ns):
   n=int(h['samples'][j]);a=b[off:off+2*n];off+=2*n
   if h['label'][j]=='EDF Annotations':annotations.append(a.decode())
   data[j].extend(np.frombuffer(a,dtype='<i2'))
 idx=[j for j in range(ns) if h['label'][j]!='EDF Annotations']
 assert all(h['unit'][j]=='uV' for j in idx)
 assert len(set(h['samples'][idx]))==1
 x=np.column_stack([(np.array(data[j],float)-h['dmin'][j])*(h['pmax'][j]-h['pmin'][j])/(h['dmax'][j]-h['dmin'][j])+h['pmin'][j] for j in idx])
 return x,[h['label'][j].replace('-CPz','') for j in idx],h['samples'][idx[0]]/dur,nr*dur

def write(name,rows):
 with (out/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
quality=[];epochs=[];summaries=[];spectra=[];inventory=[];agg=[];raw={}
for cond,file in files.items():
 x,ch,fs,dur=read_edf(source/file);raw[cond]=(x,ch,fs);n=int(4*fs)
 inventory.append(dict(condition=cond,duration_s=dur,fs_hz=fs,signal_channels=len(ch)))
 xx=x[:len(x)//n*n].reshape(-1,n,len(ch))
 for j,c in enumerate(ch):quality.append(dict(condition=cond,channel=c,median_sd_uV=np.median(np.std(xx[:,:,j],axis=1,ddof=1)),median_ptp_uV=np.median(np.ptp(xx[:,:,j],axis=1)),fraction_ptp_gt150=np.mean(np.ptp(xx[:,:,j],axis=1)>150)))
 cs=[c for c in ch if c not in ['F3','T8','M1','M2']];ci=[ch.index(c) for c in cs];ri=[cs.index(c) for c in roi]
 for sc in ['primary','strict100','matched280','all_available']:
  limit=280 if sc=='matched280' else dur;threshold=100 if sc=='strict100' else 150
  starts=list(range(0,int(limit//4)*4,4))
  if sc!='all_available':starts=starts[1:-1]
  pp={'scalp':[],'posterior':[]}
  for t in starts:
   z=x[int(t*fs):int((t+4)*fs),ci];ptp=np.ptp(z,axis=0);flat=np.std(z,axis=0,ddof=1)<.1;jump=np.max(abs(np.diff(z,axis=0)),axis=0)>50
   good=(ptp<=threshold)&~flat&~jump
   f,p=periodogram(z,fs=fs,window='hann',detrend='constant',axis=0,scaling='density')
   epochs.append(dict(condition=cond,scenario=sc,start_s=t,keep_global=bool(all(good)),keep_posterior=bool(all(good[ri])),n_bad_channels=sum(~good),max_ptp_uV=max(ptp)))
   if all(good):pp['scalp'].append(p)
   if all(good[ri]):pp['posterior'].append(p[:,ri])
  for reg,arr in pp.items():
   if not arr:continue
   avg=np.mean(arr,axis=0);cc=cs if reg=='scalp' else roi
   for band,(lo,hi) in bands.items():
    val=np.sum(avg[(f>=lo)&(f<hi)],axis=0)*fs/n;total=np.sum(avg[(f>=1)&(f<30)],axis=0)*fs/n;rel=100*val/total
    for j,c in enumerate(cc):summaries.append(dict(condition=cond,scenario=sc,region=reg,channel=c,band=band,power_uV2=val[j],relative_pct=rel[j],retained_epochs=len(arr),retained_seconds=4*len(arr)))
    agg.append(dict(condition=cond,scenario=sc,region=reg,band=band,power_uV2=np.mean(val),relative_pct=np.mean(rel),retained_epochs=len(arr),retained_seconds=4*len(arr)))
   if sc=='primary':
    for hz,power in zip(f,np.mean(avg,axis=1)):spectra.append(dict(condition=cond,region=reg,frequency_hz=hz,psd_uV2_Hz=power))
contrasts=[]
for sc in ['primary','strict100','matched280','all_available']:
 for reg in ['scalp','posterior']:
  for band in bands:
   for a,b in [('TCF','EC'),('EC','EO')]:
    select=lambda c:next(v for v in agg if v['condition']==c and v['scenario']==sc and v['region']==reg and v['band']==band)
    u,v=select(a),select(b)
    contrasts.append(dict(scenario=sc,region=reg,band=band,contrast=a+'_vs_'+b,change_pct=100*(u['power_uV2']/v['power_uV2']-1),change_dB=10*np.log10(u['power_uV2']/v['power_uV2']),relative_change_pp=u['relative_pct']-v['relative_pct']))
for name,rows in [('recordings',inventory),('channel_quality',quality),('epoch_quality',epochs),('channel_bandpower',summaries),('regional_bandpower',agg),('spectra',spectra),('contrasts',contrasts)]:write(name+'.csv',rows)
colors={'EO':'#2874a6','EC':'#169b82','TCF':'#c45d28'}
fig,axes=plt.subplots(1,2,figsize=(12,4.5),constrained_layout=True)
for ax,reg in zip(axes,['scalp','posterior']):
 for c in files:
  a=[v for v in spectra if v['condition']==c and v['region']==reg and 1<=v['frequency_hz']<=30]
  ax.plot([v['frequency_hz'] for v in a],10*np.log10([v['psd_uV2_Hz'] for v in a]),label=c,color=colors[c])
 ax.set(title=reg.capitalize()+' | accepted epochs',xlabel='Frequency (Hz)',ylabel='PSD (dB relative to 1 µV²/Hz)');ax.grid(alpha=.2);ax.legend()
fig.savefig(out/'spectra.png',dpi=180);plt.close(fig)
fig,axes=plt.subplots(3,1,figsize=(12,7),constrained_layout=True)
for ax,c in zip(axes,files):
 x,ch,fs=raw[c];t=np.arange(len(x))/fs
 for j,k in enumerate(['Fp1','F3','T8','O1']):
  z=x[:,ch.index(k)];ax.plot(t[::8],z[::8]-np.median(z)+j*250,lw=.35,label=k)
 ax.set(title=c+' | raw traces, median-centred; 250 µV offsets',xlabel='Time (s)',ylabel='µV + offset');ax.legend(ncol=4,loc='upper right')
fig.savefig(out/'raw_quality.png',dpi=180);plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(12,4.5),constrained_layout=True)
for ax,reg in zip(axes,['scalp','posterior']):
 for i,c in enumerate(files):
  a=[next(v for v in agg if v['condition']==c and v['scenario']=='primary' and v['region']==reg and v['band']==b)['power_uV2'] for b in bands]
  ax.bar(np.arange(4)+(i-1)*.25,a,width=.24,label=c,color=colors[c])
 ax.set_xticks(range(4),bands);ax.set(title=reg.capitalize(),ylabel='Absolute band power (µV²)');ax.legend();ax.grid(axis='y',alpha=.2)
fig.savefig(out/'bandpower.png',dpi=180);plt.close(fig)
(out/'python_versions.json').write_text(json.dumps(dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__,matplotlib=matplotlib.__version__),indent=2))
print(json.dumps([v for v in agg if v['scenario']=='primary'],indent=2))
