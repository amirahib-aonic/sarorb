import pandas as pd, numpy as np, sys
d=pd.read_csv(sys.argv[1])
p=d.pivot_table(index=['year','month'],columns='sensor',values='hotspots',aggfunc='sum')
idx=pd.MultiIndex.from_product([range(2002,2027),range(1,13)],names=['year','month'])
p=p.reindex(idx)
last={s:d[d.sensor==s][['year','month']].apply(tuple,axis=1).max() for s in d.sensor.unique()}
first={s:d[d.sensor==s][['year','month']].apply(tuple,axis=1).min() for s in d.sensor.unique()}
print('first',first,'last',last)
def span(s):
    m=[(i>=first[s]) and (i<=last[s]) for i in p.index]
    return m
for s in p.columns: p.loc[span(s),s]=p.loc[span(s),s].fillna(0)
p=p.rename(columns={'MODIS':'M','VIIRS S-NPP':'S','VIIRS NOAA-20':'N'})
o=p.dropna(subset=['M','S']).copy()
print('overlap months',len(o), o.index[0], o.index[-1])
print('annual'); a=o.groupby('year')[['M','S']].sum(); a['r']=a.S/a.M; print(a.round(2).to_string())
print('pearson log', np.corrcoef(np.log1p(o.M),np.log1p(o.S))[0,1].round(3))
print('global ratio', (o.S.sum()/o.M.sum()).round(3))
mr=o.groupby(level='month').apply(lambda g:g.S.sum()/max(g.M.sum(),1)); print('month ratio',mr.round(2).to_dict())
dry=[7,8,9,10]
def fit(tr):
    g=tr.S.sum()/tr.M.sum()
    m=tr.groupby(level='month').apply(lambda x:x.S.sum()/max(x.M.sum(),1))
    sd=tr[tr.index.get_level_values('month').isin(dry)]; sw=tr[~tr.index.get_level_values('month').isin(dry)]
    s2=(sd.S.sum()/sd.M.sum(), sw.S.sum()/sw.M.sum())
    b,a=np.polyfit(np.log1p(tr.M),np.log1p(tr.S),1)
    return g,m,s2,(a,b)
def pred(te,f):
    g,m,s2,(a,b)=f; mo=te.index.get_level_values('month')
    return {'global':te.M*g,'per_month':te.M*m.reindex(mo).values,'dry_wet':te.M*np.where(mo.isin(dry),s2[0],s2[1]),'loglog':np.expm1(a+b*np.log1p(te.M))}
res={k:[] for k in ['global','per_month','dry_wet','loglog']}; ann={k:[] for k in res}
full_years=[y for y in sorted(set(o.index.get_level_values('year'))) if (o.loc[y].shape[0]==12)]
for y in full_years:
    tr=o.drop(index=y,level='year'); te=o.loc[[y]]
    pr=pred(te,fit(tr))
    for k,v in pr.items():
        res[k].append(pd.DataFrame({'y':te.S.values,'p':np.asarray(v)}))
        ann[k].append((y,te.S.sum(),float(np.sum(v))))
print('LOYO years',full_years)
for k in res:
    r=pd.concat(res[k]); e=r.p-r.y
    an=pd.DataFrame(ann[k],columns=['y','obs','pred']); ape=(an.pred-an.obs).abs()/an.obs
    print(f"{k}: monthly MAE={e.abs().mean():.0f} medAE={e.abs().median():.0f} logRMSE={np.sqrt(np.mean((np.log1p(r.p)-np.log1p(r.y))**2)):.3f} annual MAPE={ape.mean()*100:.1f}% medAPE={ape.median()*100:.1f}% worst={an.loc[ape.idxmax(),'y']}:{ape.max()*100:.0f}%")
g,m,s2,ab=fit(o); print('full fit global',round(g,3),'drywet',[round(x,3) for x in s2],'loglog a,b',[round(x,3) for x in ab])
b_=o.dropna(subset=['N']) if 'N' in o else None
sn=p.dropna(subset=['S','N']); print('SNPP vs N20 months',len(sn),'ratio N/S',round(sn.N.sum()/sn.S.sum(),3),'corr log',np.corrcoef(np.log1p(sn.S),np.log1p(sn.N))[0,1].round(3))
pre=p.loc[2002:2011,'M']; print('pre2012 MODIS annual', pre.groupby(level='year').sum().to_dict())
print('harmonized pre2012 per_month', (pre*m.reindex(pre.index.get_level_values('month')).values).groupby(level='year').sum().round(0).to_dict())
