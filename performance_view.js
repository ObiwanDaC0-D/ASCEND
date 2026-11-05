/* ASCEND V7 performance display: additive and read-only. */
(function(){
  const original=HTMLButtonElement.prototype;
  const button=document.getElementById('launch');
  if(!button)return;
  const panel=document.createElement('section');
  panel.id='v7-lab';
  panel.style.cssText='text-align:left;margin:18px 0';
  document.getElementById('results').after(panel);
  button.addEventListener('click',async()=>{
    panel.replaceChildren();
    try{
      const response=await fetch('./data/latest.json?lab='+Date.now(),{cache:'no-store'});
      if(!response.ok)return;
      const d=await response.json();
      if(d.version!==7)return;
      const p=d.performance;
      if(!p||p.status!=='tracking')return;
      const details=document.createElement('details');
      details.style.cssText='background:#15233d;border:1px solid #304569;border-radius:16px;padding:18px';
      const summary=document.createElement('summary');
      summary.textContent='Portfolio research · five-stock baskets';
      details.append(summary);
      const paragraph=(value)=>{const e=document.createElement('p');e.style.cssText='color:#c1cee4;font-size:.9rem;line-height:1.55';e.textContent=value;details.append(e)};
      paragraph('Prospectively recorded signal dates: '+p.signal_days+'. Outcomes use hypothetical next-session closing entries, not executable trades.');
      for(const h of ['2','5']){
        const c=p.cohorts?.[h];if(!c)continue;
        const value=x=>x===null||x===undefined?'pending':x.toFixed(3)+'%';
        paragraph(h+'-session horizon · '+c.completed_cohorts+' complete five-stock baskets · mean net '+value(c.average_basket_net_pct)+' · mean excess vs SPY '+value(c.average_basket_excess_pct));
        if(c.uncertainty_95_pct)paragraph('Exploratory 95% block-bootstrap range: '+c.uncertainty_95_pct.map(value).join(' to ')+'. Overlapping dates can remain dependent.');
        else paragraph('Uncertainty range appears after 20 complete baskets.');
        const recent=c.cohorts||[];
        if(recent.length){
          const table=document.createElement('table');
          table.style.cssText='width:100%;font-size:.8rem;border-collapse:collapse;margin-top:10px';
          const head=document.createElement('tr');
          for(const name of ['Signal day','Basket net','vs SPY']){const cell=document.createElement('th');cell.textContent=name;cell.style.textAlign='left';cell.style.padding='7px 4px';head.append(cell)}
          table.append(head);
          for(const row of recent.slice(-5).reverse()){
            const tr=document.createElement('tr');
            for(const v of [row.signal_date,row.basket_net_pct+'%',row.excess_pct+'%']){const td=document.createElement('td');td.textContent=v;td.style.padding='7px 4px';tr.append(td)}
            table.append(tr)
          }
          details.append(table)
        }
      }
      paragraph('Research averages are not a compounded, capital-constrained portfolio. Costs assume 10 basis points round trip. No established forecasting advantage.');
      panel.append(details)
    }catch(error){console.warn('ASCEND optional performance view unavailable',error)}
  });
})();
