/* Koersbepaling v2 — shared sync logic (SSE + state) */

const PARTICIPANTS = {
  Sophie:'#E57373', Rinske:'#64B5F6', Jesper:'#81C784',
  Frank:'#FFB74D', Anne:'#BA68C8', Louise:'#4DB6AC'
};

const STICKY_COLORS = {
  yellow:'#FFF9C4', green:'#C8E6C9', blue:'#BBDEFB',
  pink:'#F8BBD0', orange:'#FFE0B2', purple:'#E1BEE7'
};

let state = { version:0, currentSlide:'welkom', participants:{}, votes:{}, stickies:{}, texts:{} };
let myName = null;
let eventSource = null;

let onStateChange = null;
let onSlideChange = null;
var onReset = null;

function connectSSE() {
  if (eventSource) eventSource.close();
  eventSource = new EventSource('api/stream');

  eventSource.addEventListener('init', e => {
    state = JSON.parse(e.data);
    if (onStateChange) onStateChange('init', state);
    if (onSlideChange) onSlideChange(state.currentSlide);
  });

  eventSource.addEventListener('message', e => {
    const u = JSON.parse(e.data);
    if (u.type === 'reset') {
      state = { version:0, currentSlide:'welkom', participants:{}, votes:{}, stickies:{}, texts:{} };
      if (onReset) { onReset(); } else if (myName) { push({ type:'join', name: myName }); }
      if (onStateChange) onStateChange('init', state);
      if (onSlideChange) onSlideChange('welkom');
      return;
    }
    applyLocal(u);
    if (onStateChange) onStateChange(u.type, u);
    if (u.type === 'navigate' && onSlideChange) onSlideChange(u.slide);
  });

  eventSource.onerror = () => { eventSource.close(); setTimeout(connectSSE, 2000); };
}

function applyLocal(u) {
  const t = u.type;
  if (t === 'join') {
    state.participants[u.name] = { color: PARTICIPANTS[u.name], online: true, lastSeen: Date.now()/1000 };
  } else if (t === 'vote') {
    if (!state.votes[u.id]) state.votes[u.id] = {};
    state.votes[u.id][u.author] = u.direction;
  } else if (t === 'unvote') {
    if (state.votes[u.id]) delete state.votes[u.id][u.author];
  } else if (t === 'sticky_add') {
    if (!state.stickies[u.zone]) state.stickies[u.zone] = {};
    state.stickies[u.zone][u.id] = { text: u.text||'', color: u.color, author: u.author||'' };
  } else if (t === 'sticky_update') {
    if (state.stickies[u.zone]?.[u.id]) state.stickies[u.zone][u.id].text = u.text;
  } else if (t === 'sticky_delete') {
    if (state.stickies[u.zone]) delete state.stickies[u.zone][u.id];
  } else if (t === 'text') {
    state.texts[u.id] = u.value;
  } else if (t === 'navigate') {
    state.currentSlide = u.slide;
  }
  state.version++;
}

function push(update) {
  fetch('api/update', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify(update)
  }).catch(()=>{});
}

function joinSession(name) {
  myName = name;
  localStorage.setItem('v2-name', name);
  push({ type:'join', name });
  setInterval(() => { if (myName) push({ type:'heartbeat', name: myName }); }, 10000);
}

function castVote(sid, direction) {
  if (!myName) return;
  if (state.votes[sid]?.[myName] === direction) {
    push({ type:'unvote', id:sid, author:myName });
  } else {
    push({ type:'vote', id:sid, direction, author:myName });
  }
}

function doAddSticky(zoneId, color) {
  const author = myName || 'Facilitator';
  const id = `s-${Date.now()}-${Math.random().toString(36).slice(2,6)}`;
  push({ type:'sticky_add', zone:zoneId, id, text:'', color, author });
  return id;
}

function doUpdateSticky(zone, id, text) {
  push({ type:'sticky_update', zone, id, text });
}

function doDeleteSticky(zone, id) {
  push({ type:'sticky_delete', zone, id });
}

let _txtTimers = {};
function doUpdateText(id, value) {
  clearTimeout(_txtTimers[id]);
  _txtTimers[id] = setTimeout(() => push({ type:'text', id, value }), 400);
}
function doFlushText(id, value) {
  clearTimeout(_txtTimers[id]);
  push({ type:'text', id, value });
}

function navigateSlide(slideId) {
  push({ type:'navigate', slide: slideId });
}

function voteCounts(sid) {
  const v = state.votes[sid] || {};
  const c = { up:0, side:0, down:0 };
  const who = { up:[], side:[], down:[] };
  for (const [name, dir] of Object.entries(v)) { c[dir]++; who[dir].push(name); }
  return { counts:c, voters:who };
}

function myVote(sid) {
  return myName ? (state.votes[sid]?.[myName] || null) : null;
}

function voterDots(names) {
  return names.map(n =>
    `<span class="voter-dot" style="background:${PARTICIPANTS[n]||'#999'}" title="${n}">${n[0]}</span>`
  ).join('');
}

function updateVoteDisplay(sid) {
  const { counts, voters } = voteCounts(sid);
  ['up','side','down'].forEach(d => {
    const ce = document.getElementById(`vc-${sid}-${d}`);
    if (ce) ce.textContent = counts[d];
    const ae = document.getElementById(`va-${sid}-${d}`);
    if (ae) ae.innerHTML = voterDots(voters[d]);
  });
  if (myName) {
    const mv = myVote(sid);
    document.querySelectorAll(`#stelling-${sid} .vote-btn`).forEach(b => {
      b.classList.toggle('selected', b.dataset.dir === mv);
    });
  }
}

var onParticipantClick = null;

function updateParticipantDots() {
  const el = document.getElementById('participantDots');
  if (!el) return;
  el.innerHTML = Object.entries(PARTICIPANTS).map(([name, color]) => {
    const p = state.participants[name];
    const online = p && (Date.now()/1000 - p.lastSeen < 30);
    const click = onParticipantClick ? `onclick="onParticipantClick('${name}')" style="background:${color};cursor:pointer;"` : `style="background:${color};"`;
    return `<button type="button" class="participant-dot ${online?'online':'offline'}" ${click} title="${name}" data-participant="${name}">${name[0]}</button>`;
  }).join('');
}

function getPersonData(name) {
  const votes = [];
  for (const [sid, voters] of Object.entries(state.votes || {})) {
    if (voters[name]) votes.push({ id: sid, direction: voters[name] });
  }
  const stickies = [];
  for (const [zone, items] of Object.entries(state.stickies || {})) {
    for (const [sId, data] of Object.entries(items)) {
      if (data.author === name) stickies.push({ zone, id: sId, text: data.text, color: data.color });
    }
  }
  return { votes, stickies };
}
