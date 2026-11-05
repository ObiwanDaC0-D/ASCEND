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
  stats.append(text("span","$"+fmt(p.price,2)+" close"),text("span",fmt(p.momentum_5d_pct,2)+"% · 5-day momentum"));
  card.append(stats);
  const more=text("details","","more");
  more.append(text("summary","Why this stock?"));
  more.append(line("20-day trend",fmt(p.trend_20d_pct,2)+"%"));
  more.append(line("Annualized volatility",fmt(p.volatility_20d_pct,1)+"%"));
  more.append(line("20-day dollar volume","$"+Math.round(Number(p.liquidity_usd)||0).toLocaleString()));
  if(p.validation?.holdout)more.append(line("Historical holdout","SPY-relative average "+fmt(p.validation.holdout.average_excess_vs_spy_pct,2)+"%; "+p.validation.holdout.signals+" qualifying observations (not a forecast)"));
  if(p.news?.headlines?.length){const n=text("details","");n.append(text("summary","Recent headlines"));const ul=text("ul","");for(const h of p.news.headlines)ul.append(text("li",h));n.append(ul);more.append(n)}
  if(p.institutional?.form4_count_90d!=null)more.append(line("SEC Form 4 filings (90 days)",p.institutional.form4_count_90d+" filings, not confirmed purchases"));
  card.append(more);return card;
}
function renderResearch(d){
  const lab=text("details","","research");
  lab.append(text("summary","Research & performance"));
  const p=d.performance;
  if(!p||p.status!=="tracking"){lab.append(text("p","Performance journal unavailable or awaiting its first successful run."));return lab}
  lab.append(text("p",p.signal_days+" recorded signal days · hypothetical next-session closing entries."));
  for(const h of ["2","5"]){
    const c=p.cohorts?.[h],r=p.risk?.[h];if(!c)continue;
    const sec=text("section","","research-group");
    sec.append(text("h3",h+"-session evaluation"));
    if(!c.completed_cohorts){sec.append(text("p","Awaiting complete five-stock outcomes."));lab.append(sec);continue}
    sec.append(line("Completed baskets",c.completed_cohorts));
    sec.append(line("Mean net",fmt(c.average_basket_net_pct,3)+"%"));
    sec.append(line("Mean excess vs SPY",fmt(c.average_basket_excess_pct,3)+"%"));
    if(r?.completed_cohorts){sec.append(line("Negative baskets",fmt(100*r.negative_fraction,1)+"%"));sec.append(line("Worst basket",fmt(r.worst_net_pct,2)+"%"));
      const seq=r.sequential_illustration;
      if(seq?.cohorts)sec.append(line("Non-overlapping illustration",seq.cohorts+" baskets · drawdown "+fmt(seq.max_drawdown_pct,2)+"% (not a tradeable account)"));
      const cost=text("details","");cost.append(text("summary","Cost assumptions"));for(const x of r.cost_sensitivity||[])cost.append(line(x.round_trip_bps+" bps round trip",fmt(x.mean_basket_net_pct,3)+"% mean net"));sec.append(cost)}
    if(c.uncertainty_95_pct)sec.append(line("Exploratory uncertainty",c.uncertainty_95_pct.map(v=>fmt(v,2)+"%").join(" to ")));
    lab.append(sec)
  }
  const marks=p.daily_marks;if(marks?.recent_paths?.length){const detail=text("details","");detail.append(text("summary","Recent paper observations"));for(const path of marks.recent_paths.slice(-3).reverse()){const m=path.marks?.at(-1);if(m)detail.append(line(path.signal_date,m.date+" · "+fmt(m.basket_net_pct,2)+"% net · "+path.strategy_id))}lab.append(detail)}
  if(d.alternative_lab){const detail=text("details","");detail.append(text("summary","Experimental research"));detail.append(text("p","Alternative-data relationships are exploratory and do not affect the rankings."));lab.append(detail)}
  lab.append(text("p","Descriptive paper research only. Overlapping selections, estimated costs, and historical adjusted closes do not establish a trading advantage.","fine"));
  return lab;
}
launch.addEventListener("click",async()=>{
  launch.disabled=true;results.replaceChildren();statusEl.textContent="Loading the latest published scan…";
  try{
    const controller=new AbortController();const timeout=setTimeout(()=>controller.abort(),18000);
    let response;try{response=await fetch("./data/latest.json?ts="+Date.now(),{cache:"no-store",signal:controller.signal})}finally{clearTimeout(timeout)}
    if(!response.ok)throw Error("The published research snapshot is unavailable.");
    const d=await response.json();
    if(d.version!==10){statusEl.textContent="An updated scan is needed. Run the daily scan in GitHub Actions.";return}
    if(d.status!=="ok"||!Array.isArray(d.picks)||d.picks.length!==5){statusEl.textContent=d.message||"No complete five-stock scan is available.";return}
    if(d.data_quality?.status!=="passed"){statusEl.textContent="The latest scan has not passed data-quality checks.";return}
    const generated=new Date(d.generated_at);
    if(!Number.isFinite(generated.getTime()))throw Error("The scan timestamp is invalid.");
    const age=Date.now()-generated.getTime();
    const dateLabel=d.price_as_of||"unknown session";
    statusEl.textContent="Market data: "+dateLabel+" · Published "+generated.toLocaleString();
    if(age>72*3600*1000)results.append(text("p","This scan is more than 72 hours old. Treat the selections as stale.","alert"));
    results.append(text("h2","The Five","results-title"));
    for(const pick of d.picks.slice(0,5))results.append(renderPick(pick));
    results.append(renderResearch(d));
  }catch(err){statusEl.textContent=err.name==="AbortError"?"The request timed out. Try again.":"Unable to load research: "+err.message}
  finally{launch.disabled=false}
});
