let selectedProfile = "strong_manager";
let competencies = [];

async function getJSON(url, options){
  const res = await fetch(url, options);
  if(!res.ok) throw new Error(await res.text());
  return await res.json();
}

function esc(value){
  return String(value ?? "").replace(/[&<>"']/g, ch => ({
    "&":"&amp;",
    "<":"&lt;",
    ">":"&gt;",
    '"':"&quot;",
    "'":"&#039;"
  }[ch]));
}

function levelLabel(level){
  return {
    critical_gap:"критический пробел",
    basic:"базовый уровень",
    working:"рабочий уровень",
    strong:"сильный уровень"
  }[level] || level;
}

function trackLabel(track){
  return {
    full_basic_track:"базовый трек",
    basic_plus_practice:"теория + практика",
    targeted_practice_track:"точечная практика",
    control_case_track:"контрольный кейс"
  }[track] || track;
}

function listHtml(items, title){
  if(!items || !items.length){
    return `
      <div class="feedback-section">
        <strong>${esc(title)}</strong>
        <p class="muted">Нет данных.</p>
      </div>
    `;
  }

  return `
    <div class="feedback-section">
      <strong>${esc(title)}</strong>
      <ul>${items.map(x => `<li>${esc(x)}</li>`).join("")}</ul>
    </div>
  `;
}

async function init(){
  const profiles = await getJSON('/api/demo-profiles');
  const profileBox = document.getElementById('profiles');

  profileBox.innerHTML = profiles.map(p => `
    <div class="profile-card ${p.profile_id===selectedProfile ? 'active' : ''}" data-id="${esc(p.profile_id)}">
      <strong>${esc(p.name)}</strong>
      <p>${esc(p.description)}</p>
    </div>
  `).join('');

  profileBox.querySelectorAll('.profile-card').forEach(card => {
    card.onclick = () => {
      selectedProfile = card.dataset.id;
      init();
    };
  });

  competencies = await getJSON('/api/roles/b2b_sales_manager/competencies');

  document.getElementById('competencySelect').innerHTML = competencies.map(c => `
    <option value="${esc(c.competency_id)}">${esc(c.name)}</option>
  `).join('');
}

async function runDiagnostic(){
  const result = await getJSON('/api/diagnostic/run-demo', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({
      role_id:'b2b_sales_manager',
      profile_id:selectedProfile
    })
  });

  document.getElementById('summary').innerHTML = `
    <strong>${esc(result.overall_summary)}</strong><br>
    Статус готовности: <span class="badge">${esc(result.readiness_status)}</span>
  `;

  document.getElementById('competencies').innerHTML = result.competency_results.map(r => `
    <div class="competency">
      <strong>${esc(r.competency_name)}</strong>
      <div class="bar"><span style="width:${(r.score/3)*100}%"></span></div>
      <span class="badge">${esc(r.score)}/3 · ${esc(levelLabel(r.level))}</span>
      <p>${esc(r.recommendation)}</p>
    </div>
  `).join('');

  document.getElementById('track').innerHTML = result.learning_track.slice(0,8).map(m => `
    <div class="module">
      <strong>${esc(m.competency_name)}</strong><br>
      <span class="badge">${esc(trackLabel(m.track_type))}</span>
      <p>${esc(m.goal)}</p>
      <small>Материалы: ${esc((m.materials || []).map(x => x.title).join(', '))}</small>
    </div>
  `).join('');
}

async function checkAnswer(){
  const payload = {
    competency_id: document.getElementById('competencySelect').value,
    question: document.getElementById('questionInput').value,
    answer: document.getElementById('answerInput').value
  };

  const result = await getJSON('/api/control/check-answer', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify(payload)
  });

  const materials = (result.recommended_materials || []).map(m => `
    <li>
      <strong>${esc(m.title || m.material_id)}</strong>
      <div class="muted">${esc(m.material_id || "")}</div>
    </li>
  `).join("");

  const sources = (result.source_chunks || []).slice(0, 3).map((src, i) => `
    <li>
      <strong>${i + 1}. ${esc(src.title || src.source_id || "Источник базы знаний")}</strong>
      <p class="muted">${esc((src.text || "").slice(0, 260))}${(src.text || "").length > 260 ? "..." : ""}</p>
    </li>
  `).join("");

  document.getElementById('checkResult').innerHTML = `
    <div class="feedback-card">
      <div class="feedback-top">
        <div>
          <span class="feedback-label">Оценка ответа</span>
          <h3>${esc(result.score)} / ${esc(result.max_score)}</h3>
        </div>
        <span class="status-pill">${esc(levelLabel(result.level))}</span>
      </div>

      <div class="feedback-main">
        <strong>Обратная связь</strong>
        <p>${esc(result.feedback)}</p>
      </div>

      <div class="feedback-grid">
        ${listHtml(result.matched_points, "Что учтено в ответе")}
        ${listHtml(result.missing_points, "Чего не хватает")}
      </div>

      <div class="feedback-section">
        <strong>Рекомендуемые материалы</strong>
        <ul>${materials || '<li class="muted">Материалы не найдены.</li>'}</ul>
      </div>

      <details class="source-details">
        <summary>Показать источники из базы знаний</summary>
        <ul>${sources || '<li class="muted">Источники не найдены.</li>'}</ul>
      </details>
    </div>
  `;
}

document.getElementById('runBtn').onclick = runDiagnostic;
document.getElementById('checkBtn').onclick = checkAnswer;

init().then(runDiagnostic).catch(err => console.error(err));
