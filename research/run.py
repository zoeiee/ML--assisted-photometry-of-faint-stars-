"""Run from repository root: python -m research.run [--stage all|data|classical|train|evaluate|experiments|figures]."""
import argparse,json,hashlib,platform,time,joblib
from pathlib import Path
import numpy as np,pandas as pd,torch
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from .core import generate,measure,metrics,FEATURES
from .models import CNN,inputs
ROOT=Path(__file__).resolve().parents[1]
C=json.loads((ROOT/'configs/default.json').read_text())
D=ROOT/'data';R=ROOT/'results'
def save(p,x):p.write_text(json.dumps(x,indent=2))
def dataset():
    for j,(split,n) in enumerate([('train',C['n_train']),('val',C['n_val']),('test',C['n_test'])]):
        im,m=generate(n,C['seed']+j);np.savez_compressed(D/f'{split}.npz',images=im,flux=[a['flux'] for a in m]);pd.DataFrame(m).to_csv(D/f'{split}_metadata.csv',index=False)
        print('Generated',split,n,flush=True)
def classical():
    for s in ['train','val','test']:
        d=np.load(D/f'{s}.npz');f=[]
        for i,im in enumerate(d['images']):
            f.append(measure(im))
            if (i+1)%1000==0:print('Measured',s,i+1,flush=True)
        np.save(D/f'{s}_features.npy',f)
def train():
    torch.set_num_threads(2);torch.manual_seed(C['seed']);np.random.seed(C['seed']);torch.use_deterministic_algorithms(True)
    a=np.load(D/'train.npz');v=np.load(D/'val.npz');f=np.load(D/'train_features.npy');fv=np.load(D/'val_features.npy')
    selected={}
    for name,cols,residual in [('Ridge',list(range(9)),False),('Residual',list(range(9)),True),('Ablation', [0,2,3,8],False)]:
        candidates=[]
        for alpha in [0.1,1.,10.,100.]:
            model=make_pipeline(StandardScaler(),Ridge(alpha=alpha));model.fit(f[:,cols],a['flux']-(f[:,1] if residual else 0))
            pred=model.predict(fv[:,cols])+(fv[:,1] if residual else 0);candidates.append((metrics(v['flux'],pred)['mae'],alpha,model))
        loss,alpha,model=min(candidates,key=lambda x:x[0]);joblib.dump(dict(model=model,cols=cols,residual=residual),R/'models'/f'{name}.joblib');selected[name]=dict(alpha=alpha,validation_mae=loss)
    x=inputs(torch.tensor(a['images']));y=torch.tensor(a['flux']/1000.,dtype=torch.float32);vx=inputs(torch.tensor(v['images']));vy=torch.tensor(v['flux']/1000.,dtype=torch.float32)
    model=CNN();opt=torch.optim.Adam(model.parameters(),lr=C['learning_rate']);history=[];best=float('inf');wait=0
    for epoch in range(C['epochs']):
        model.train();total=0
        for ix in torch.randperm(len(x)).split(C['batch_size']):
            opt.zero_grad();loss=((model(x[ix])-y[ix])**2).mean();loss.backward();opt.step();total+=loss.item()*len(ix)
        model.eval()
        with torch.no_grad():vl=float(((model(vx)-vy)**2).mean())
        history.append(dict(epoch=epoch+1,train_mse_scaled=total/len(x),val_mse_scaled=vl));print('Epoch',epoch+1,'val MSE',vl,flush=True)
        if vl<best:
            best=vl;wait=0;torch.save(dict(state_dict=model.state_dict(),config=C,epoch=epoch+1,input_scale=100.,target_scale=1000.),R/'models/stellar_cnn.pt')
        else:wait+=1
        if wait>=C['patience']:break
    save(R/'models/selection.json',selected);pd.DataFrame(history).to_csv(R/'models/history.csv',index=False)
def predict(images,f):
    torch.set_num_threads(2);m=CNN();m.load_state_dict(torch.load(R/'models/stellar_cnn.pt',map_location='cpu',weights_only=True)['state_dict']);m.eval()
    with torch.no_grad():cnn=m(inputs(torch.tensor(images))).numpy()*1000.
    out={'Aperture':f[:,0],'PSF':f[:,1],'CNN':cnn}
    for name in ['Ridge','Residual','Ablation']:
        b=joblib.load(R/'models'/f'{name}.joblib');out[name]=b['model'].predict(f[:,b['cols']])+(f[:,1] if b['residual'] else 0)
    return out
def evaluate():
    d=np.load(D/'test.npz');f=np.load(D/'test_features.npy');out=predict(d['images'],f);table=pd.read_csv(D/'test_metadata.csv');summary={}
    rng=np.random.default_rng(C['seed']);ix=rng.integers(0,len(f),(C['bootstrap_repetitions'],len(f)))
    for name,p in out.items():
        table[name]=p;summary[name]=metrics(d['flux'],p);err=abs(p-d['flux']);summary[name]['mae_95_bootstrap']=np.quantile(err[ix].mean(1),[.025,.975]).tolist()
        delta=err-abs(out['PSF']-d['flux']);summary[name]['mae_minus_psf_95_paired']=np.quantile(delta[ix].mean(1),[.025,.975]).tolist()
    table.to_csv(R/'metrics/test_predictions.csv',index=False);save(R/'metrics/summary.json',summary)
    save(R/'metrics/quality.json',{'fit_failure_count':int(f[:,9].sum()),'test_count':len(f)})
    print(json.dumps(summary,indent=2),flush=True)
def experiments():
    scenarios={'faint':{'flux':150.},'bright':{'flux':2000.},'sky_high':{'sky':100.},'read_high':{'read':10.},'wide_psf':{'sigma':2.2},'elliptical':{'ratio':.65,'theta':.6},'moffat':{'shape':'moffat'},'crowded':{'neighbor':.7},'gradient':{'gradient':.5},'control':{}}
    rows=[]
    # Common seed couples latent nuisance parameters; Poisson draws need not stay paired across scenarios.
    for name,over in scenarios.items():
        im,meta=generate(C['experiment_n'],C['seed']+10,**over);f=np.array([measure(a) for a in im]);out=predict(im,f);t=pd.DataFrame(meta)
        np.savez_compressed(D/f'experiment_{name}.npz',images=im,features=f)
        for method,p in out.items():t[method]=p;rows.append(dict(experiment=name,method=method,n=len(t),**metrics(t.flux.to_numpy(),p)))
        t.to_csv(R/'metrics'/f'experiment_{name}.csv',index=False);print('Experiment',name,flush=True)
    pd.DataFrame(rows).to_csv(R/'metrics/experiments.csv',index=False);save(R/'experiment_configurations.json',scenarios)
def manifest():
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in list(D.glob('*'))+list((R/'models').glob('*'))+list((R/'metrics').glob('*')) if p.is_file()}
    save(R/'experiment_manifest.json',dict(experiment_id='stellar-new-20261016',status='executed_new_synthetic_run_not_historical_reproduction',config=C,units='electrons',metric_definitions={'mae':'mean(abs(pred-truth))','rmse':'sqrt(mean((pred-truth)^2))','bias':'mean(pred-truth)','median_relative_percent':'100*median(abs(pred-truth)/truth)'},summary=json.loads((R/'metrics/summary.json').read_text()),scenario_parameters=json.loads((R/'experiment_configurations.json').read_text()) if (R/'experiment_configurations.json').exists() else {},scenario_results=pd.read_csv(R/'metrics/experiments.csv').to_dict(orient='records') if (R/'metrics/experiments.csv').exists() else [],figure_source='research/figures.py',prediction_source='results/metrics/test_predictions.csv',dataset_parameters={'shape':[32,32],'flux_distribution':'log-uniform 100–3000 electrons','sigma':'uniform 1.1–1.5 pixels','sky':20,'read_noise':3,'profile':'circular Gaussian','pixel_integration':'2x2 midpoint quadrature','normalisation':'finite stamp'},model_checkpoints={name:hashes.get('results/models/'+name) for name in ['stellar_cnn.pt','Ridge.joblib','Residual.joblib','Ablation.joblib']},sha256=hashes,python=platform.python_version(),torch=torch.__version__,real_data=False,limitations=['Single training seed','No original dataset/checkpoint supplied','Finite-stamp flux normalization','CNN budget limited','Scenario sweeps are synthetic stress tests']))
def main():
    p=argparse.ArgumentParser();p.add_argument('--stage',choices=['all','data','classical','train','evaluate','experiments','figures'],default='all');a=p.parse_args()
    for name,fn in [('data',dataset),('classical',classical),('train',train),('evaluate',evaluate),('experiments',experiments)]:
        if a.stage in ('all',name):fn()
    if a.stage in ('all','figures'):
        from .figures import figures
        figures()
    if a.stage in ('all','evaluate','experiments','figures'):manifest()
if __name__=='__main__':main()
