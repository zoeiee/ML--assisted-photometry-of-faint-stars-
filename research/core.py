"""Electron-domain, finite-stamp photometry. No truth metadata enters estimators."""
import numpy as np
from scipy.optimize import least_squares
from scipy.special import erf
Y, X = np.mgrid[:32,:32]

def psf(x=15.5,y=15.5,sigma=1.3,ratio=1.,theta=0.,shape='gaussian',size=32):
    # Four-point subpixel quadrature for general profiles. Unit sum defines
    # flux within the stamp, rather than infinite-aperture flux.
    Y, X = np.mgrid[:size,:size]
    p=np.zeros((size,size))
    for dx in [-.25,.25]:
        for dy in [-.25,.25]:
            a=(X+dx-x)*np.cos(theta)+(Y+dy-y)*np.sin(theta)
            b=-(X+dx-x)*np.sin(theta)+(Y+dy-y)*np.cos(theta)
            r=(a/sigma)**2+(b/(sigma*ratio))**2
            p+=np.exp(-r/2) if shape=='gaussian' else (1+r/(2*np.log(2)/(2**(1/3)-1)))**-3
    return p/p.sum()

def generate(n,seed,image_size=32,**overrides):
    rng=np.random.default_rng(seed); images=[]; meta=[]
    Y,X=np.mgrid[:image_size,:image_size]
    for i in range(n):
        m=dict(flux=float(np.exp(rng.uniform(np.log(100),np.log(3000)))),sky=20.,read=3.,sigma=float(rng.uniform(1.1,1.5)),ratio=1.,theta=0.,shape='gaussian',neighbor=0.,gradient=0.,x=float(rng.uniform(image_size/2-1,image_size/2)),y=float(rng.uniform(image_size/2-1,image_size/2)))
        m.update(overrides)
        source=m['flux']*psf(m['x'],m['y'],m['sigma'],m['ratio'],m['theta'],m['shape'],size=image_size)
        source+=m['neighbor']*m['flux']*psf(m['x']+4,m['y']+1,m['sigma'],size=image_size)
        expected=source+m['sky']+m['gradient']*(X-(image_size-1)/2)
        if np.any(expected<0): raise ValueError('Negative expected counts')
        image=rng.poisson(expected)+rng.normal(0,m['read'],(image_size,image_size))
        m['id']=f'{seed}:{i}';m['snr']=m['flux']/np.sqrt(m['flux']+4*np.pi*m['sigma']**2*(m['sky']+m['read']**2))
        images.append(image);meta.append(m)
    return np.asarray(images,dtype=np.float32),meta

def measure(image,radius=4.):
    r0=np.hypot(X-15.5,Y-15.5);ann=(r0>=9)&(r0<=13)
    sky=float(np.median(image[ann]));sd=float(np.std(image[ann],ddof=1))
    w=np.maximum(image-sky,0)*(r0<4)
    cx=float((w*X).sum()/max(w.sum(),1e-9));cy=float((w*Y).sum()/max(w.sum(),1e-9))
    if w.sum()==0:cx=cy=15.5
    cx=float(np.clip(cx,13.5,17.5));cy=float(np.clip(cy,13.5,17.5))
    mask=np.hypot(X-cx,Y-cy)<radius
    # A nominal calibration PSF is used, not the injected truth width.
    fraction=psf(cx,cy,1.3)[mask].sum();ap=float((image[mask]-sky).sum()/fraction)
    unc=float(np.sqrt(max((image[mask]-sky).sum(),0)+mask.sum()*sd**2+mask.sum()**2*np.pi/2*sd**2/ann.sum())/fraction)
    roi=r0<7
    def model(q):return q[0]*psf(q[1],q[2],q[3])+q[4]
    def residual(q):return (model(q)[roi]-image[roi])/max(sd,1.)
    try:
        fit=least_squares(residual,[np.clip(ap,1,19999),cx,cy,1.3,sky],bounds=([0,13,13,.6,-100],[20000,18,18,3,1000]),max_nfev=50)
        f,x,y,s,b=fit.x;flag=int(not fit.success);res=float(np.mean(residual(fit.x)**2))
    except (ValueError,RuntimeError):f,x,y,s,b=ap,cx,cy,1.3,sky;flag=1;res=0.
    return np.array([ap,f,sky,sd,s,x-15.5,y-15.5,res,unc,flag],dtype=float)

FEATURES=['aperture','psf','sky','background_sd','sigma','dx','dy','residual_mse','aperture_uncertainty','fit_failure']
def metrics(truth,pred):
    d=np.asarray(pred)-truth
    return dict(mae=float(np.mean(abs(d))),rmse=float(np.sqrt(np.mean(d*d))),bias=float(np.mean(d)),median_relative_percent=float(100*np.median(abs(d)/truth)))
