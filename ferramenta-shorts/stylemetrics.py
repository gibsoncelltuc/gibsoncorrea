#!/usr/bin/env python3
"""Style metrics on 1080x1920 frames: python3 stylemetrics.py <glob...>  -> per-metric mean/p10/p90"""
import sys,glob,numpy as np
from PIL import Image, ImageFilter
def metrics(path):
    im=Image.open(path).convert('RGB').resize((540,960)); a=np.asarray(im,np.float32)/255
    mx=a.max(2); mn=a.min(2); sat=np.where(mx>0.02,(mx-mn)/np.maximum(mx,1e-3),0)
    lum=a@np.array([.299,.587,.114],np.float32)
    g=np.asarray(im.convert('L'),np.float32)/255
    lap=np.abs(g[1:-1,1:-1]*4-g[:-2,1:-1]-g[2:,1:-1]-g[1:-1,:-2]-g[1:-1,2:])
    rg=a[...,0]-a[...,1]; yb=.5*(a[...,0]+a[...,1])-a[...,2]
    colorful=np.sqrt(rg.std()**2+yb.std()**2)+.3*np.sqrt(rg.mean()**2+yb.mean()**2)
    top=lum[:320].mean(); bot=lum[640:].mean()
    return dict(sat=sat[mx>0.1].mean(),lum_mean=lum.mean(),lum_std=lum.std(),p5=np.percentile(lum,5),p95=np.percentile(lum,95),
        dark=(lum<0.08).mean(),bright=(lum>0.92).mean(),detail=lap.mean()*10,edges=(lap>0.12).mean(),colorful=colorful,
        warm=(a[...,0].mean()-a[...,2].mean()),hues=len(np.unique((np.argmax(a,2)*7+(sat>.35)*3)[::8,::8])))
def summarize(files):
    M=[metrics(f) for f in files]; keys=M[0].keys()
    return {k:(np.mean([m[k] for m in M]),np.percentile([m[k] for m in M],10),np.percentile([m[k] for m in M],90)) for k in keys}
if __name__=='__main__':
    fs=[f for p in sys.argv[1:] for f in glob.glob(p)]
    S=summarize(fs); print(len(fs),'frames')
    for k,(m,lo,hi) in S.items(): print(f'{k:10s} mean {m:7.3f}  p10 {lo:7.3f}  p90 {hi:7.3f}')
