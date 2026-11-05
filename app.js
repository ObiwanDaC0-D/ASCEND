"use strict";
const launch=document.querySelector("#launch");
const statusEl=document.querySelector("#status");
const results=document.querySelector("#results");
const text=(tag,value,cls)=>{const e=document.createElement(tag);e.textContent=value??"";if(cls)e.className=cls;return e};
const fmt=(v,d=1)=>Number.isFinite(Number(v))?Number(v).toFixed(d):"—";
const line=(label,value)=>{const p=text("p",label+": "+value);return p};
function renderPick(p){
  const card=text("article","");card.className="pick";
  const top=text("div","","pick-head");
  top.append(text("span",String(p.rank).padStart(2,"0"),"rank"),text("strong",p.ticker,"ticker"));
  card.append(top);
  const stats=text("div","","pick-stats");
  stats.append(text("span","$"+fmt(p.price,2)+" last close"),text("span",fmt(p.momentum_5d_pct,2)+"% · 5-day change"));
  card.append(stats);
  const more=text("details","","more");
  more.append(text("summary","Details"));
  more.append(line("20-day change",fmt(p.trend_20d_pct,2)+"%"));
  more.append(line("Volatility",fmt(p.volatility_20d_pct,1)+"%"));
  more.append(line("Daily trading volume","$"+Math.round(Number(p.liquidity_usd)||0).toLocaleString()));
  if(p.validation?.holdout)more.append(line("Past results","Average vs SPY "+fmt(p.validation.holdout.average_excess_vs_spy_pct,2)+"%; "+p.validation.holdout.signals+" past signals (not a forecast)"));
  if(p.news?.headlines?.length){const n=text("details","");n.append(text("summary","News"));const ul=text("ul","");for(const h of p.news.headlines)ul.append(text("li",h));n.append(ul);more.append(n)}
  if(p.institutional?.form4_count_90d!=null)more.append(line("Insider filings (90 days)",p.institutional.form4_count_90d+" filings (not necessarily purchases)"));
  card.append(more);return card;
}
function renderResearch(d){
  const lab=text("details","","research");
  lab.append(text("summary","Performance"));
  const p=d.performance;
  if(!p||p.status!=="tracking"){lab.append(text("p","Not enough results yet."));return lab}
  lab.append(text("p",p.signal_days+" days tracked · simulated entries at the next day's close."));
  for(const h of ["2","5"]){
    const c=p.cohorts?.[h],r=p.risk?.[h];if(!c)continue;
    const sec=text("section","","research-group");
    sec.append(text("h3",h+"-day results"));
    if(!c.completed_cohorts){sec.append(text("p","Waiting for more data."));lab.append(sec);continue}
    sec.append(line("Completed groups",c.completed_cohorts));
    sec.append(line("Average return",fmt(c.average_basket_net_pct,3)+"%"));
    sec.append(line("Compared with SPY",fmt(c.average_basket_excess_pct,3)+"%"));
    if(r?.completed_cohorts){sec.append(line("Groups that lost value",fmt(100*r.negative_fraction,1)+"%"));sec.append(line("Largest loss",fmt(r.worst_net_pct,2)+"%"));
      const seq=r.sequential_illustration;
      if(seq?.cohorts)sec.append(line("Sample sequence",seq.cohorts+" baskets · drawdown "+fmt(seq.max_drawdown_pct,2)+"% (not a tradeable account)"));
      const cost=text("details","");cost.append(text("summary","Trading costs"));for(const x of r.cost_sensitivity||[])cost.append(line(x.round_trip_bps+" bps round trip",fmt(x.mean_basket_net_pct,3)+"% mean net"));sec.append(cost)}
    if(c.uncertainty_95_pct)sec.append(line("Estimated range",c.uncertainty_95_pct.map(v=>fmt(v,2)+"%").join(" to ")));
    lab.append(sec)
  }
  const marks=p.daily_marks;if(marks?.recent_paths?.length){const detail=text("details","");detail.append(text("summary","Recent results"));for(const path of marks.recent_paths.slice(-3).reverse()){const m=path.marks?.at(-1);if(m)detail.append(line(path.signal_date,m.date+" · "+fmt(m.basket_net_pct,2)+"% net · "+path.strategy_id))}lab.append(detail)}
  if(d.alternative_lab){const detail=text("details","");detail.append(text("summary","Other experiments"));detail.append(text("p","These experiments do not affect the five picks."));lab.append(detail)}
  lab.append(text("p","Simulated results, not actual trades. Past performance does not predict future returns.","fine"));
  return lab;
}
launch.addEventListener("click",async()=>{
  launch.disabled=true;results.replaceChildren();statusEl.textContent="Loading…";
  try{
    const controller=new AbortController();const timeout=setTimeout(()=>controller.abort(),18000);
    let response;try{response=await fetch("./data/latest.json?ts="+Date.now(),{cache:"no-store",signal:controller.signal})}finally{clearTimeout(timeout)}
    if(!response.ok)throw Error("No results have been published yet.");
    const d=await response.json();
    if(d.version!==10){statusEl.textContent="New results aren't ready yet.";return}
    if(d.status!=="ok"||!Array.isArray(d.picks)||d.picks.length!==5){statusEl.textContent=d.message||"No picks available yet.";return}
    if(d.data_quality?.status!=="passed"){statusEl.textContent="Results unavailable: data check failed.";return}
    const generated=new Date(d.generated_at);
    if(!Number.isFinite(generated.getTime()))throw Error("The scan timestamp is invalid.");
    const age=Date.now()-generated.getTime();
    const dateLabel=d.price_as_of||"unknown session";
    statusEl.textContent="Prices from "+dateLabel+" · Updated "+generated.toLocaleString();
    if(age>72*3600*1000)results.append(text("p","These results may be outdated.","alert"));
    results.append(text("h2","Today's five","results-title"));
    for(const pick of d.picks.slice(0,5))results.append(renderPick(pick));
    results.append(renderResearch(d));
  }catch(err){statusEl.textContent=err.name==="AbortError"?"Loading took too long. Try again.":"Could not load results: "+err.message}
  finally{launch.disabled=false}
});
