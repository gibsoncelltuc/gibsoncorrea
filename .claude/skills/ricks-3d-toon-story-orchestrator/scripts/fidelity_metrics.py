import numpy as np, subprocess, sys, json
from PIL import Image
def load_ref():
    out=[]
    for pre in 'AB':
        for k in range(0,8):
            t=k*1.0+0.3; i=int(round(t*59.94))+1
            try: im=Image.open(f'./{pre}_{i:03d}.png').convert('RGB').resize((360,648)); out.append(np.asarray(im).astype(np.float32)/255)
            except Exception: pass
    return out
def load_video(path, n=21):
    out=[]
    for k in range(n):
        t=k*1.0+0.3
        raw=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',path,'-frames:v','1','-vf','scale=360:648','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
        if len(raw)==360*648*3: out.append(np.frombuffer(raw,np.uint8).reshape(648,360,3).astype(np.float32)/255)
    return out
def metrics(fr):
    res={'laplacian_var':[], 'edge_density':[], 'colorfulness':[], 'sat_mean':[], 'val_mean':[], 'contrast_local':[], 'vignette':[]}
    for a in fr:
        a=np.concatenate([a[:int(648*.62)],a[int(648*.78):]])
        L=0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]
        lap=(-4*L[1:-1,1:-1]+L[:-2,1:-1]+L[2:,1:-1]+L[1:-1,:-2]+L[1:-1,2:]); res['laplacian_var'].append(float(lap.var()*1e3))
        gx=np.abs(L[:,1:]-L[:,:-1])[:-1]; gy=np.abs(L[1:]-L[:-1])[:,:-1]; g=np.hypot(gx,gy); res['edge_density'].append(float((g>0.06).mean()))
        rg=a[...,0]-a[...,1]; yb=0.5*(a[...,0]+a[...,1])-a[...,2]; res['colorfulness'].append(float(np.sqrt(rg.std()**2+yb.std()**2)+0.3*np.sqrt(rg.mean()**2+yb.mean()**2)))
        mx=a.max(2); mn=a.min(2); s=(mx-mn)/(mx+1e-6); res['sat_mean'].append(float(s.mean())); res['val_mean'].append(float(mx.mean()))
        H,W=L.shape; b=L[:H//12*12,:W//12*12].reshape(H//12,12,W//12,12).std(axis=(1,3)); res['contrast_local'].append(float(b.mean()))
        h,w=L.shape; c=L[h//3:2*h//3,w//3:2*w//3].mean(); e=np.concatenate([L[:h//6].ravel(),L[-h//6:].ravel()]).mean(); res['vignette'].append(float(c/(e+1e-6)))
    return {k:round(float(np.mean(v)),4) for k,v in res.items()}
if __name__=='__main__':
    R=load_ref(); mr=metrics(R); out={'ref':mr}
    for name,path in [a.split('=') for a in sys.argv[1:]]:
        M=load_video(path); out[name]=metrics(M); print(name,'quadros',len(M))
    print('quadros ref',len(R)); print(f"{'métrica':16s}"+''.join(f"{k:>14s}" for k in out))
    for k in mr: print(f"{k:16s}"+''.join(f"{out[n][k]:14.4f}" for n in out))
    json.dump(out,open('./metrics.json','w'),indent=1)
