import json
from pathlib import Path
import numpy as np
import pytest
from research.core import psf,generate,measure,metrics
P=Path(__file__).resolve().parents[1]
@pytest.mark.parametrize('shape',['gaussian','moffat'])
def test_flux(shape):
    p=psf(15.2,15.8,1.4,.8,.4,shape)
    assert p.min()>=0
    assert np.isclose(p.sum(),1,atol=1e-12)
    assert np.isclose((1234*p).sum(),1234)
def test_reproducibility():
    a,m=generate(3,5);b,n=generate(3,5);assert np.array_equal(a,b);assert m==n
    c,_=generate(3,6);assert not np.array_equal(a,c)
def test_noise():
    a,_=generate(500,99,flux=0.,sky=30.,read=4.)
    assert abs(a.mean()-30)<.1
    assert abs(a.var()-46)<.6

def test_units():
    from astropy import units as u
    flux=1000*u.electron
    assert np.isclose((flux*psf()).sum().to_value(u.electron),1000)
def test_aperture_and_fit():
    im=2000*psf()+20
    f=measure(im)
    assert abs(f[0]-2000)<1
    assert abs(f[1]-2000)<1
    assert f[9]==0

def test_photutils_crosscheck():
    from photutils.aperture import CircularAperture,aperture_photometry
    im=psf();mask=np.hypot(*np.mgrid[-15.5:16.5,-15.5:16.5])<4
    p=aperture_photometry(im,CircularAperture((15.5,15.5),r=4),method='center')
    assert np.isclose(p['aperture_sum'][0],im[mask].sum())
def test_metric():
    m=metrics(np.array([1.,2.]),np.array([2.,0.]));assert m['mae']==1.5;assert m['bias']==-.5;assert m['rmse']==np.sqrt(2.5)
def test_splits():
    import pandas as pd
    ids=[set(pd.read_csv(P/'data'/f'{s}_metadata.csv').id) for s in ['train','val','test']]
    assert len(ids[0])==7000 and len(ids[1])==1000 and len(ids[2])==2000
    assert all(not ids[i]&ids[j] for i,j in [(0,1),(0,2),(1,2)])
def test_checkpoint():
    import torch
    from research.models import CNN
    p=P/'results/models/stellar_cnn.pt'
    if not p.exists():pytest.skip('training pending')
    m=CNN();m.load_state_dict(torch.load(p,map_location='cpu',weights_only=True)['state_dict']);assert torch.isfinite(m(torch.zeros(2,1,32,32))).all()
def test_manifest():
    p=P/'results/experiment_manifest.json'
    if not p.exists():pytest.skip('evaluation pending')
    m=json.loads(p.read_text());assert m['units']=='electrons';assert m['real_data'] is False
    import hashlib
    for name,sha in m['sha256'].items():assert hashlib.sha256((P/name).read_bytes()).hexdigest()==sha

def test_configurable_image_size():
    a,_=generate(2,1,image_size=40)
    assert a.shape==(2,40,40)
    assert np.isclose(psf(size=40).sum(),1)

def test_scaler_training_only():
    import joblib
    p=P/'results/models/Ridge.joblib'
    if not p.exists():pytest.skip('training pending')
    obj=joblib.load(p);x=np.load(P/'data/train_features.npy')[:,obj['cols']]
    assert np.allclose(obj['model'][0].mean_,x.mean(axis=0))
    assert obj['model'][0].n_samples_seen_==7000

def test_prediction_pairing_and_saved_metrics():
    import pandas as pd
    p=P/'results/metrics/test_predictions.csv'
    if not p.exists():pytest.skip('evaluation pending')
    t=pd.read_csv(p);meta=pd.read_csv(P/'data/test_metadata.csv');s=json.loads((P/'results/metrics/summary.json').read_text())
    assert t.id.to_list()==meta.id.to_list()
    for name,v in s.items():
        assert np.isfinite(t[name]).all()
        assert np.isclose(metrics(t.flux.to_numpy(),t[name].to_numpy())['mae'],v['mae'])
