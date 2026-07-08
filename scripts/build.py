#!/usr/bin/env python3
"""Generate dist/index.html from data/skills.json (content) + data/profiles.json (illustrative ratings).
Content is authored in Notion, mirrored into data/skills.json, then baked into a self-contained dashboard."""
import json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
skills = json.loads((root/'data'/'skills.json').read_text())
profiles = json.loads((root/'data'/'profiles.json').read_text())
DATA = {**skills, **profiles}
data_js = json.dumps(DATA, ensure_ascii=False)

TEMPLATE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Experience team competency</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root{
  --bg-app:#ffffff; --bg-subtle:#fafafa; --bg-elevated:#f4f4f5; --border:#d4d4d8;
  --text:#09090b; --muted:#52525b; --placeholder:#71717a;
  --primary:#ff5200; --focus:#3b82f6; --grid:#ffffff; --bar-muted:#e4e4e7;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg-app);color:var(--text);font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;font-size:14px;line-height:24px;letter-spacing:.1px;}
.wrap{max-width:760px;margin:0 auto;padding:24px 20px 64px;}
.head{display:flex;align-items:center;gap:12px;padding-bottom:16px;}
.dot{width:12px;height:12px;border-radius:3px;background:var(--primary);}
h1{font-size:26px;line-height:34px;font-weight:800;letter-spacing:.2px;margin:0;}
.filters{display:flex;gap:16px;flex-wrap:wrap;margin:20px 0 10px;align-items:flex-end;}
.fld{display:flex;flex-direction:column;gap:8px;}
.fld label{font:700 12px/20px Inter;letter-spacing:.1px;}
.fld select{height:36px;min-width:210px;padding:0 38px 0 12px;border-radius:8px;border:1px solid var(--border);background:var(--bg-app);color:var(--text);font:400 14px/24px Inter;cursor:pointer;appearance:none;-webkit-appearance:none;-moz-appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%2352525b' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 12px center;}
.fld select:focus{outline:none;border-color:var(--focus);box-shadow:0 0 0 2px var(--focus);}
.fld select:disabled{opacity:.55;cursor:not-allowed;}
.datanote{display:flex;align-items:flex-start;gap:7px;color:var(--muted);font:500 12px/18px Inter;margin:8px 0 0;}
.datanote svg{width:14px;height:14px;flex:none;margin-top:2px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;}
.datanote b{color:var(--text);font-weight:700;}
.domlegend{display:flex;flex-wrap:wrap;gap:14px;margin:4px 0 4px;}
.domlegend span{display:inline-flex;align-items:center;gap:6px;font:700 12px/18px Inter;}
.domlegend i{width:11px;height:11px;border-radius:3px;display:inline-block;}
.hint{color:var(--muted);font-size:12px;line-height:18px;margin:6px 0 0;}
.hints{display:flex;flex-wrap:wrap;gap:6px 16px;margin:8px 0 0;}
.hintitem{display:inline-flex;align-items:center;gap:6px;color:var(--muted);font:500 12px/18px Inter;}
.hicon{width:14px;height:14px;flex:none;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;}
.chartwrap{position:relative;margin-top:4px;}
.tip{position:absolute;display:none;pointer-events:none;width:250px;background:var(--bg-app);border:1px solid var(--border);border-radius:10px;padding:0;overflow:hidden;box-shadow:0 10px 15px -3px rgba(16,24,40,.12),0 4px 6px -4px rgba(16,24,40,.12);z-index:30;}
.tiphead{padding:10px 12px 8px;}
.tiptitle{font:800 13px/17px Inter;}
.tipdom{font:700 11px/16px Inter;}
.tipsum{font:400 11px/15px Inter;color:var(--muted);margin-top:3px;}
.bars{display:flex;align-items:flex-end;gap:3px;height:26px;margin-top:8px;}
.bar{flex:1;border-radius:2px 2px 0 0;}
.tipcur{font:600 11px/15px Inter;padding:8px 12px;color:#fff;}
.detail{margin-top:20px;padding-top:18px;}
.dhead{display:flex;align-items:center;justify-content:space-between;gap:10px;}
.dtitle{font:800 20px/26px Inter;letter-spacing:.2px;margin:0;}
.badge{display:inline-flex;align-items:center;gap:6px;padding:3px 10px;border-radius:999px;font:700 11px/16px Inter;}
.ddef{font-size:14px;line-height:22px;margin:8px 0 2px;}
.dsum{font-size:13px;line-height:20px;color:var(--muted);font-style:italic;margin:0 0 4px;}
.clear{background:none;border:none;color:var(--primary);font:600 13px/18px Inter;cursor:pointer;padding:0;}
.dcur{display:flex;align-items:center;gap:12px;margin:14px 0;padding:10px 12px;border-radius:8px;color:#fff;}
.dcur .bars{height:22px;width:80px;margin:0;}
.lv{padding:12px 0;}
.lvtop{display:flex;align-items:center;gap:10px;}
.lvbars{margin:6px 0 0;}
.lvbars .bars{width:66px;height:18px;margin:0;gap:2px;}
.lvnum{font:800 12px/18px Inter;min-width:74px;}
.lvname{font:700 13px/20px Inter;}
.lvsent{font-size:13.5px;line-height:21px;margin:3px 0 0 84px;}
.lvex{font-size:12.5px;line-height:19px;color:var(--muted);margin:3px 0 0 84px;}
.lvon{border-radius:10px;padding:12px 14px;margin:0 -14px;}
.domgroup{padding:10px 0;}
.domname{display:inline-flex;align-items:center;gap:6px;font:800 13px/20px Inter;}
.domdot{width:11px;height:11px;border-radius:3px;display:inline-block;}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;}
.chip{font:600 11px/16px Inter;padding:5px 11px;border:1px solid var(--border);background:var(--bg-app);color:var(--text);border-radius:999px;cursor:pointer;transition:border-color .12s,color .12s;}
.chip:hover{border-color:var(--primary);color:var(--primary);}
.toast{position:fixed;left:50%;top:28px;transform:translateX(-50%) translateY(-20px);background:var(--text);color:var(--bg-app);font:600 13px/18px Inter;padding:10px 16px;border-radius:999px;box-shadow:0 10px 15px -3px rgba(0,0,0,.2);opacity:0;pointer-events:none;cursor:pointer;transition:opacity .2s,transform .2s;z-index:50;}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0);pointer-events:auto;}
svg text{cursor:pointer;}
</style>
</head>
<body>
<div class="wrap">
  <div class="head"><div class="dot"></div><h1>Experience team competency</h1></div>
  <div class="filters">
    <div class="fld"><label for="fPerson">Team member</label><select id="fPerson"></select></div>
    <div class="fld"><label for="fRole">Role</label><select id="fRole"></select></div>
    <div class="fld"><label for="fLevel">Level</label><select id="fLevel"></select></div>
  </div>
  <div class="datanote" id="dataNote" style="display:none"></div>
  <div class="domlegend" id="domlegend"></div>
  <div class="hints">
    <span class="hintitem"><svg class="hicon" viewBox="0 0 24 24" aria-hidden="true"><path d="M4.037 4.688a.495.495 0 0 1 .651-.651l16 6.5a.5.5 0 0 1-.063.947l-6.124 1.58a2 2 0 0 0-1.438 1.435l-1.579 6.126a.5.5 0 0 1-.947.063z"/></svg>Hover for a quick look</span>
    <span class="hintitem"><svg class="hicon" viewBox="0 0 24 24" aria-hidden="true"><path d="m9 9 5 12 1.774-5.226L21 14z"/><path d="m16.071 16.071 4.243 4.243"/><path d="m7.188 2.239.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656-2.12 2.122"/></svg>Click to select &amp; see full detail</span>
    <span class="hintitem"><svg class="hicon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m15 9-6 6M9 9l6 6"/></svg>Click again to clear</span>
  </div>
  <div class="chartwrap"><div id="chart"></div><div id="tip" class="tip"></div></div>
  <section class="detail" id="detail"></section>
</div>
<div class="toast" id="toast"></div>

<script>
const DATA = /*__DATA__*/;
const SK=DATA.skills, N=SK.length, MAX=5;
const LEVELS=DATA.levels, LMEAN=DATA.levelMeaning, DOMAINS=DATA.domains;
const domColor={}; DOMAINS.forEach(d=>domColor[d.name]=d.color);
const PROF=DATA.profiles, ROLE_OPTS=DATA.roleOptions, LEVEL_OPTS=DATA.levelOptions, MEMBERS=DATA.members||[];
const cx=380,cy=380,R=205,rIn=34,slice=360/N,ring=(R-rIn)/MAX;
let fRole=ROLE_OPTS[0], fLevel='Senior', fPerson='', selected=null;

function esc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function pol(r,deg){const a=deg*Math.PI/180;return [cx+r*Math.sin(a),cy-r*Math.cos(a)];}
function annular(ri,ro,a1,a2){const p1=pol(ro,a1),p2=pol(ro,a2),p3=pol(ri,a2),p4=pol(ri,a1);const la=(a2-a1)>180?1:0;
 return `M${p1[0].toFixed(1)} ${p1[1].toFixed(1)} A${ro} ${ro} 0 ${la} 1 ${p2[0].toFixed(1)} ${p2[1].toFixed(1)} L${p3[0].toFixed(1)} ${p3[1].toFixed(1)} A${ri} ${ri} 0 ${la} 0 ${p4[0].toFixed(1)} ${p4[1].toFixed(1)} Z`;}
function currentMember(){return fPerson?(MEMBERS.find(m=>m.name===fPerson)||null):null;}
function profile(){const m=currentMember(); if(m){return {title:m.name, cur:m.cur, target:m.target, role:m.role, level:m.level, quarter:m.quarter, source:m.source, member:true};} return PROF[fRole+'|'+fLevel]||null;}
function sentence(i,k){return (SK[i].L[k]||'').split('|')[0];}
function example(i,k){const p=(SK[i].L[k]||'').split('|');return p.length>1?p[1]:'';}
function splitLabel(name){ if(name.length<=20) return [name]; const mid=name.length/2; let best=-1,bd=99;
  for(let p=0;p<name.length;p++){ if(name[p]===' '){const d=Math.abs(p-mid); if(d<bd){bd=d;best=p;}} }
  if(best<0) return [name]; return [name.slice(0,best), name.slice(best+1)]; }
function barsHTML(cur,dcol,h){h=h||26; let s=`<div class="bars" style="height:${h}px">`;
  for(let k=0;k<MAX;k++){const on=cur&&k<cur; s+=`<div class="bar" style="height:${40+k*15}%;background:${on?dcol:'var(--bar-muted)'}"></div>`;} return s+'</div>';}

function drawChart(){
 const host=document.getElementById('chart'), grid=cssbg(), text='#09090b';
 const prof=profile(); let s='';
 for(let i=0;i<N;i++){const a1=i*slice-slice/2,a2=i*slice+slice/2,col=domColor[SK[i].domain];
   const op = selected===null?1:(i===selected?1:0.28);
   s+=`<g class="skg" data-i="${i}" style="opacity:${op};transition:opacity .12s">`;
   s+=`<path d="${annular(rIn,R,a1,a2)}" fill="${col}" opacity="0.10"/>`;
   if(prof){const lv=prof.cur[i]; if(lv>0){const ro=rIn+lv*ring; s+=`<path d="${annular(rIn,ro,a1,a2)}" fill="${col}" opacity="${i===selected?0.95:0.8}"/>`;}}
   s+=`<path d="${annular(rIn,R,a1,a2)}" fill="transparent" style="cursor:pointer"/></g>`;}
 for(let k=0;k<=MAX;k++){const rr=rIn+k*ring; s+=`<circle cx="${cx}" cy="${cy}" r="${rr.toFixed(1)}" fill="none" stroke="${grid}" stroke-width="${(k===0||k===MAX)?1.6:1}" opacity="0.85"/>`;}
 for(let i=0;i<N;i++){const ang=i*slice-slice/2,p1=pol(rIn,ang),p2=pol(R,ang); s+=`<line x1="${p1[0].toFixed(1)}" y1="${p1[1].toFixed(1)}" x2="${p2[0].toFixed(1)}" y2="${p2[1].toFixed(1)}" stroke="${grid}" stroke-width="1" opacity="0.7"/>`;}
 s+=`<circle cx="${cx}" cy="${cy}" r="${rIn}" fill="${cssel()}" stroke="${grid}" stroke-width="1.6"/>`;
 DOMAINS.forEach(d=>{const a1=d.start*slice-slice/2,a2=d.end*slice+slice/2; s+=`<path class="dband" data-dom="${d.name}" d="${annular(R+2,R+9,a1,a2)}" fill="${d.color}" opacity="0.9" style="transition:opacity .12s"/>`;});
 [0,4,9,13,15].forEach(k=>{const ang=k*slice-slice/2,p1=pol(rIn,ang),p2=pol(R+9,ang); s+=`<line x1="${p1[0].toFixed(1)}" y1="${p1[1].toFixed(1)}" x2="${p2[0].toFixed(1)}" y2="${p2[1].toFixed(1)}" stroke="${cssbg()}" stroke-width="3"/>`;});
 if(prof&&prof.target){for(let i=0;i<N;i++){const t=prof.target[i]; if(t>0){const a1=i*slice-slice/2+2,a2=i*slice+slice/2-2,rr=rIn+t*ring,col=domColor[SK[i].domain];
   const pa=pol(rr,a1),pb=pol(rr,a2),top=selected===null||selected===i;
   s+=`<path d="M${pa[0].toFixed(1)} ${pa[1].toFixed(1)} A${rr.toFixed(1)} ${rr.toFixed(1)} 0 0 1 ${pb[0].toFixed(1)} ${pb[1].toFixed(1)}" fill="none" stroke="${col}" stroke-width="2.5" stroke-dasharray="4 3" stroke-linecap="round" opacity="${top?0.95:0.22}"/>`;}}}
 if(selected!==null){const a1=selected*slice-slice/2,a2=selected*slice+slice/2; s+=`<path d="${annular(rIn,R,a1,a2)}" fill="none" stroke="${domColor[SK[selected].domain]}" stroke-width="3" stroke-linejoin="round"/>`;}
 for(let i=0;i<N;i++){const ang=i*slice,lp=pol(R+14,ang); let rot=ang-90,anc='start'; if(rot>90&&rot<270){rot+=180;anc='end';}
   const on=selected===i, col=on?domColor[SK[i].domain]:text, lines=splitLabel(SK[i].skill);
   s+=`<g class="lblg" data-i="${i}" style="cursor:pointer;opacity:${selected===null?1:(on?1:0.28)};transition:opacity .12s"><text x="${lp[0].toFixed(1)}" y="${lp[1].toFixed(1)}" transform="rotate(${rot.toFixed(1)} ${lp[0].toFixed(1)} ${lp[1].toFixed(1)})" text-anchor="${anc}" dominant-baseline="middle" font-size="16" font-weight="${on?800:600}" fill="${col}">`;
   if(lines.length===1){s+=`<tspan x="${lp[0].toFixed(1)}">${esc(lines[0])}</tspan>`;}
   else{s+=`<tspan x="${lp[0].toFixed(1)}" dy="-0.35em">${esc(lines[0])}</tspan><tspan x="${lp[0].toFixed(1)}" dy="1.15em">${esc(lines[1])}</tspan>`;}
   s+=`</text></g>`;}
 host.innerHTML=`<svg viewBox="0 0 760 760" width="100%" style="max-width:600px;display:block;margin:0 auto" xmlns="http://www.w3.org/2000/svg">${s}</svg>`;
 attachHover();
 setHover(null);
}
function cssbg(){return getComputedStyle(document.documentElement).getPropertyValue('--bg-app').trim();}
function cssel(){return getComputedStyle(document.documentElement).getPropertyValue('--bg-elevated').trim();}

function setHover(i){const idx=(i!==null)?i:selected, dom=idx===null?null:SK[idx].domain;
  document.querySelectorAll('#chart .skg, #chart .lblg').forEach(x=>{const j=+x.dataset.i;
    x.style.opacity = i!==null ? (j===i?'1':'0.15') : (selected===null?'1':(j===selected?'1':'0.28'));});
  document.querySelectorAll('#chart .dband').forEach(b=>{b.style.opacity = dom===null?'0.9':(b.dataset.dom===dom?'1':'0.22');});
  document.querySelectorAll('#domlegend span').forEach(sp=>{sp.style.opacity = dom===null?'1':(sp.dataset.dom===dom?'1':'0.3');});}
function attachHover(){const tip=document.getElementById('tip'), wrap=document.querySelector('.chartwrap');
 function showTip(i){const sk=SK[i],prof=profile(),cur=prof?prof.cur[i]:null,tgt=prof&&prof.target?prof.target[i]:null,dcol=domColor[sk.domain];
   let h=`<div class="tiphead"><div class="tiptitle">${esc(sk.skill)}</div><div class="tipdom" style="color:${dcol}">${sk.domain}</div><div class="tipsum">${esc(sk.summary)}</div>${barsHTML(cur,dcol)}</div>`;
   if(cur){h+=`<div class="tipcur" style="background:${dcol}">Level ${cur} of 5 &middot; ${LEVELS[cur-1]}${tgt?` &middot; target ${tgt}`:''}: ${esc(sentence(i,cur-1))}</div>`;}
   tip.innerHTML=h; tip.style.display='block';}
 function moveTip(e){const r=wrap.getBoundingClientRect(),tw=tip.offsetWidth,th=tip.offsetHeight;
   let x=e.clientX-r.left+16; if(x+tw>r.width)x=e.clientX-r.left-tw-16; if(x<2)x=2;
   let y=e.clientY-r.top+16; if(y+th>r.height)y=r.height-th-2; if(y<2)y=2; tip.style.left=x+'px'; tip.style.top=y+'px';}
 document.querySelectorAll('#chart .skg, #chart .lblg').forEach(g=>{const i=+g.dataset.i;
   g.addEventListener('mouseenter',()=>{setHover(i);showTip(i);});
   g.addEventListener('mousemove',moveTip);
   g.addEventListener('mouseleave',()=>{setHover(null);tip.style.display='none';});
   g.addEventListener('click',()=>{ if(selected===i){deselect();} else {selectSkill(i);} });
 });
}
window.selectSkill=function(i){selected=i;drawChart();renderDetail();
 const d=document.getElementById('detail'); const r=d.getBoundingClientRect();
 if(r.top>window.innerHeight-90||r.bottom<60){showToast('Tap to view details \u2193');}};
function deselect(){selected=null;drawChart();renderDetail();}
let toastT=null;
function showToast(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');
 if(toastT)clearTimeout(toastT); toastT=setTimeout(()=>t.classList.remove('show'),2600);}
function dismissToast(){const t=document.getElementById('toast');t.classList.remove('show');if(toastT)clearTimeout(toastT);}

function renderDetail(){const d=document.getElementById('detail');
 if(selected===null){let h=`<h2 class="dtitle" style="font-size:16px;line-height:24px">Domains &amp; criteria</h2><p class="hint">The 19 skills grouped by domain. Hover the radar for a quick look, or pick a skill here.</p>`;
   DOMAINS.forEach(dm=>{h+=`<div class="domgroup"><span class="domname" style="color:${dm.color}"><span class="domdot" style="background:${dm.color}"></span>${dm.name}</span><span class="chips">`;
     for(let i=dm.start;i<=dm.end;i++){h+=`<button class="chip" onclick="selectSkill(${i})">${esc(SK[i].skill)}</button>`;} h+=`</span></div>`;});
   d.innerHTML=h; return;}
 const sk=SK[selected],dcol=domColor[sk.domain],prof=profile(),cur=prof?prof.cur[selected]:null;
 let h=`<div class="dhead"><h2 class="dtitle">${esc(sk.skill)}</h2><button class="clear" onclick="deselect()">Clear \u2715</button></div>`;
 h+=`<div style="margin:6px 0 0"><span class="badge" style="background:${dcol}1f;color:${dcol}">${sk.domain}</span> <span class="badge" style="background:var(--bg-elevated);color:var(--muted)">${sk.track}</span></div>`;
 h+=`<p class="ddef">${esc(sk.definition)}</p><p class="dsum">${esc(sk.summary)}</p>`;
 if(cur){const tgt=prof.target?prof.target[selected]:null,gap=tgt?tgt-cur:null;
   h+=`<div class="dcur" style="background:${dcol}">${barsHTML(cur,'#ffffff',22)}<div><div style="font-weight:800">Current for ${esc(prof.title)}${prof.quarter?` &middot; ${esc(prof.quarter)}`:''}</div><div style="font-size:12px;opacity:.92">Level ${cur} of 5 &middot; ${LEVELS[cur-1]}${tgt?` &middot; target ${tgt} (${LEVELS[tgt-1]})${gap>0?` &middot; gap +${gap}`:''}`:''}</div></div></div>`;}
 for(let k=0;k<MAX;k++){const on=cur&&(k+1)===cur;
   h+=`<div class="lv ${on?'lvon':''}" style="${on?`background:${dcol}1f`:''}"><div class="lvtop"><span class="lvnum" style="color:${dcol}">LEVEL ${k+1}</span><span class="lvname">${LEVELS[k]}</span></div><div class="lvbars">${barsHTML(k+1,dcol,18)}</div>`;
   h+=`<div class="lvsent">${esc(sentence(selected,k))}</div>`;
   const ex=example(selected,k); if(ex)h+=`<div class="lvex"><b>GHN example:</b> ${esc(ex)}</div>`;
   h+=`</div>`;}
 d.innerHTML=h;}

function fillSelect(id,opts,val){const el=document.getElementById(id);el.innerHTML='';opts.forEach(o=>{const op=document.createElement('option');op.value=o;op.textContent=o;if(o===val)op.selected=true;el.appendChild(op);});}
function availableLevels(role){return LEVEL_OPTS.filter(l=>PROF[role+'|'+l]);}
function refreshLevels(){const av=availableLevels(fRole); if(!av.includes(fLevel))fLevel=av[0]; fillSelect('fLevel',av,fLevel);}
function onRole(){fRole=document.getElementById('fRole').value;refreshLevels();selected=null;drawChart();renderDetail();}
function onLevel(){fLevel=document.getElementById('fLevel').value;selected=null;drawChart();renderDetail();}
function fillPersonSelect(){const el=document.getElementById('fPerson');el.innerHTML='';
 const opts=[['','Benchmark (role & level)']].concat(MEMBERS.map(m=>[m.name,m.name+' · '+m.level]));
 opts.forEach(([v,label])=>{const o=document.createElement('option');o.value=v;o.textContent=label;if(v===fPerson)o.selected=true;el.appendChild(o);});}
function updateDataNote(){const el=document.getElementById('dataNote'),m=currentMember();
 if(!m){el.style.display='none';el.innerHTML='';return;}
 const icon='<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>';
 const txt=m.source==='seed'
   ?`<span><b>Seed estimate</b> for ${esc(m.name)} — derived from the ${esc(m.role)} · ${esc(m.level)} benchmark, pending real ratings from Notion. Dashed arc = target.</span>`
   :`<span>${esc(m.name)}’s ${esc(m.quarter||'')} ratings from Notion. Dashed arc = target.</span>`;
 el.style.display='flex';el.innerHTML=icon+txt;}
function onPerson(){fPerson=document.getElementById('fPerson').value;const m=currentMember();
 const rl=document.getElementById('fRole'),lv=document.getElementById('fLevel');
 if(m){fRole=m.role;refreshLevels();if(availableLevels(fRole).includes(m.level))fLevel=m.level;fillSelect('fLevel',availableLevels(fRole),fLevel);rl.value=fRole;rl.disabled=true;lv.disabled=true;}
 else{rl.disabled=false;lv.disabled=false;}
 selected=null;updateDataNote();drawChart();renderDetail();}
function build(){
 fillPersonSelect();fillSelect('fRole',ROLE_OPTS,fRole);refreshLevels();
 document.getElementById('fPerson').onchange=onPerson;
 document.getElementById('fRole').onchange=onRole;document.getElementById('fLevel').onchange=onLevel;
 document.getElementById('domlegend').innerHTML=DOMAINS.map(d=>`<span data-dom="${d.name}" style="color:${d.color};transition:opacity .12s"><i style="background:${d.color}"></i>${d.name}</span>`).join('');
 document.getElementById('toast').onclick=()=>{document.getElementById('detail').scrollIntoView({behavior:'smooth',block:'start'});dismissToast();};
 updateDataNote();drawChart();renderDetail();}
build();
</script>
</body>
</html>'''

html = TEMPLATE.replace('/*__DATA__*/', data_js)
(root/'dist'/'index.html').write_text(html)
print("built dist/index.html", len(html), "bytes")
