from pathlib import Path
import numpy as np,pandas as pd,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .core import psf,measure
P=Path(__file__).resolve().parents[1];R=P/'results';F=R/'figures'
COLORS=['#386b85','#d49343','#577a5c','#9a6075','#77679a']
METHODS=['Aperture','PSF','Ridge','Residual','CNN']
def finish(fig,name):
    fig.tight_layout();fig.savefig(F/(name+'.svg'),bbox_inches='tight');fig.savefig(F/(name+'.png'),dpi=160,bbox_inches='tight');plt.close(fig)
def figures():
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    t=pd.read_csv(R/'metrics/test_predictions.csv');d=np.load(P/'data/test.npz');f=np.load(P/'data/test_features.npy')
    ix=int(np.argmin(abs(t.flux-500)));im=d['images'][ix];q=f[ix];source=q[1]*psf(q[5]+15.5,q[6]+15.5,q[4]); yy,xx=np.mgrid[:32,:32]; roi=np.hypot(xx-15.5,yy-15.5)<7; fit=source+np.mean((im-source)[roi])
    fig,ax=plt.subplots(1,3,figsize=(10,3));
    for a,z,title in zip(ax,[im,fit,im-fit],['Observed CCD cutout','Fitted Gaussian + sky','Observed − model']):
        obj=a.imshow(z,cmap='cividis' if title!='Observed − model' else 'RdBu_r');a.set_title(title);a.set_xlabel('Pixel');fig.colorbar(obj,ax=a,label='Electrons',shrink=.7)
    finish(fig,'detector')
    fig,ax=plt.subplots(1,2,figsize=(9,3.4))
    for j,m in enumerate(METHODS):
        e=t[m]-t.flux;ax[0].bar(j,abs(e).mean(),color=COLORS[j]);ax[1].bar(j,e.mean(),color=COLORS[j])
    for a in ax:a.set_xticks(range(5),METHODS,rotation=25);a.grid(axis='y',alpha=.15);a.set_axisbelow(True)
    ax[0].set_ylabel('Mean absolute error (electrons)');ax[1].set_ylabel('Mean signed error (electrons)');ax[1].axhline(0,color='#444',lw=.8)
    finish(fig,'comparison')
    fig,ax=plt.subplots(1,2,figsize=(9,3.4))
    for m,c in zip(METHODS,COLORS):
        e=t[m]-t.flux;ax[0].hist(e,bins=np.linspace(-600,600,60),histtype='step',color=c,label=m,density=True)
        bins=pd.qcut(t.snr,6,duplicates='drop');g=pd.DataFrame({'snr':t.snr,'error':abs(e),'bin':bins}).groupby('bin',observed=True).mean(numeric_only=True)
        ax[1].plot(g.snr,g.error,'o-',label=m,color=c)
    ax[0].set_xlabel('Prediction − truth (electrons)');ax[0].set_ylabel('Density');ax[1].set_xlabel('Truth-based reference SNR');ax[1].set_ylabel('MAE (electrons)');ax[1].legend(frameon=False)
    finish(fig,'errors')
    h=pd.read_csv(R/'models/history.csv');fig,ax=plt.subplots(figsize=(7,3));ax.plot(h.epoch,h.train_mse_scaled,label='Training');ax.plot(h.epoch,h.val_mse_scaled,label='Validation');ax.set_xlabel('Epoch');ax.set_ylabel('MSE in (1000 electrons)²');ax.legend(frameon=False);finish(fig,'training')
    e=pd.read_csv(R/'metrics/experiments.csv');fig,ax=plt.subplots(figsize=(10,4));names=list(e.experiment.unique());x=np.arange(len(names))
    for j,(m,c) in enumerate(zip(METHODS,COLORS)):ax.bar(x+(j-2)*.15,[e[(e.experiment==n)&(e.method==m)].mae.iloc[0] for n in names],width=.15,label=m,color=c)
    ax.set_xticks(x,[n.replace('_',' ') for n in names],rotation=30,ha='right');ax.set_ylabel('MAE (electrons; log scale)');ax.set_yscale('log');ax.legend(ncol=5,frameon=False);finish(fig,'conditions')
    fig,ax=plt.subplots(figsize=(7,3));
    for m,c in zip(METHODS,COLORS):
        g=pd.DataFrame({'flux':t.flux,'relative':abs(t[m]-t.flux)/t.flux*100,'bin':pd.qcut(t.flux,6)}).groupby('bin',observed=True).median(numeric_only=True);ax.plot(g.flux,g.relative,'o-',label=m,color=c)
    ax.set_xscale('log');ax.set_xlabel('Injected flux (electrons)');ax.set_ylabel('Median absolute relative error (%)');ax.legend(frameon=False);finish(fig,'flux')
