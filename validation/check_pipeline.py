from pathlib import Path
import json, hashlib
import numpy as np
from scipy.signal import periodogram
root=Path(__file__).resolve().parents[1]
fs=256;n=1024;t=np.arange(n)/fs;x=10*np.sin(2*np.pi*10*t)
f,p=periodogram(x,fs,window='hann',detrend='constant',scaling='density')
alpha=np.sum(p[(f>=8)&(f<13)])*fs/n
assert abs(alpha-50)<1e-10
w=.5-.5*np.cos(2*np.pi*np.arange(n)/n)
a=abs(np.fft.rfft((x-x.mean())*w))**2/(fs*np.sum(w*w));a[1:-1]*=2
assert np.allclose(a,p,atol=1e-12,rtol=1e-12)
log=json.loads((root/'validation/data_integrity.json').read_text())
assert all(i['signal_and_annotation_bytes_unchanged'] for i in log)
for i in log:
 assert hashlib.sha256((root/'data/anonymized'/i['file']).read_bytes()).hexdigest()==i['sha256_header_redacted']
result=dict(sinusoid_frequency_hz=10,sinusoid_peak_amplitude_uV=10,expected_alpha_power_uV2=50,measured_alpha_power_uV2=alpha,independent_fft_max_error=float(np.max(abs(a-p))),data_integrity_records=len(log),R_execution_status='Not executed; runtime unavailable')
(root/'validation/validation_results.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
