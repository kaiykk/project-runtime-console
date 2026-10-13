(function () {
  const C = window.PrcCData;
  if (!C) return;
  const renderExecutionSteps = agents;

  function locator(event) {
    const ref = event?.evidence_ref || {};
    return ref.line ? `父 Session · line ${ref.line} · byte ${ref.byte_offset ?? '?'}` : '父侧定位不可用';
  }

  function evidenceLink(event, label) {
    if (!event) return '<div class="c-reuse-inspector boundary">当前父侧没有可打开的这类记录。</div>';
    return `<button class="evidence-link" data-c-event="${esc(event.event_id)}"><span>↗</span><span><strong>${esc(label)}</strong><small>${esc(locator(event))} · 点击查看原始记录</small></span></button>`;
  }

  let evidenceTrigger = null;
  function closeEvidence() {
    $('#modal').classList.remove('open');
    if (evidenceTrigger?.isConnected) evidenceTrigger.focus({ preventScroll: true });
    evidenceTrigger = null;
  }

  function notificationBody(event) {
    if (!event) return '';
    const text = String(event.content || '');
    const block = text.match(/<subagent_notification>\s*([\s\S]*?)\s*<\/subagent_notification>/);
    if (!block) return '';
    try {
      const notice = JSON.parse(block[1]);
      const value = typeof notice.status?.completed === 'string' ? notice.status.completed
        : typeof notice.message === 'string' ? notice.message : null;
      return value || '';
    } catch (_) { return ''; }
  }

  function selectedItem(model) {
    return model.all.find(item => item.agent.agent_id === state.selectedAgent) || null;
  }

  function representative(model, group) {
    return group.items[0] || null;
  }

  function representativeSet(model) {
    const result = [];
    model.groups.forEach(group => {
      const first = representative(model, group);
      if (first) result.push(first);
      if (group.key === 'research') {
        const second = group.items.find(item => item.agent.agent_id !== first?.agent.agent_id);
        if (second) result.push(second);
      }
    });
    return result;
  }

  function rootInspector(model) {
    const root = model.root;
    return `<div class="inspect-header"><span class="eyebrow">FOCUS INSPECTOR <span class="pill blue" style="margin-left:7px">ROOT SESSION</span></span><h2>Root Session</h2><div class="intro">主 Session 的身份和派发总览；不把父侧最终消息冒充整个运行结果。</div></div><div class="inspect-scroll"><section class="inspect-block"><h3>01 · 这张图表示什么</h3><div class="quote">${esc(model.childCount)} 个 child Agent 身份和 ${esc(model.dispatchCount)} 个有派发正文的执行者来自同一个父 Session。</div></section><section class="inspect-block"><h3>02 · 当前可确认的数量</h3><p class="intro">${esc(model.groups[0]?.items.length || 0)} 个研究任务 · ${esc(model.groups[1]?.items.length || 0)} 个审阅任务 · ${esc(model.groups[2]?.items.length || 0)} 个文档/受限产出任务。</p><div class="boundary">这些是派发内容的归类，不是完成度、质量或产品结果。失败的派发尝试没有被编成 Agent。</div></section><section class="inspect-block"><h3>03 · 证据边界</h3><div class="boundary">本阶段接入父侧派发和父侧返回通知。child API 的内部 Turn、工具记录和最后助手消息仍未接入；不会用父记录代替 child 执行记录。</div></section></div>`;
  }

  function childInspector(item) {
    const agent = item.agent;
    const task = item.task;
    const notification = item.notification;
    const childBoundary = '此视图只读取父侧派发和返回通知，尚未查询该子会话的内部执行记录。';
    return `<div class="inspect-header"><span class="eyebrow">FOCUS INSPECTOR <span class="pill purple" style="margin-left:7px">角色线索 · 待整理</span></span><h2>${esc(agent.nickname || 'Agent')}</h2><div class="intro">任务内容优先；身份编号和原始定位放在证据层。</div></div><div class="inspect-scroll"><section class="inspect-block"><h3>01 · 先看懂它要做什么</h3><div class="quote">${esc(task.title)}<br>${esc(task.summary)}</div><p class="intro" style="margin-top:9px">这是一条从真实派发正文整理出的说明，不表示任务已经完成。</p></section><section class="inspect-block"><h3>02 · 这次明确要求</h3><p><b>目的：</b>${esc(task.purpose)}</p><p><b>限制：</b>${esc(task.limits)}</p><p><b>预期交付：</b>${esc(task.deliverable)}</p></section><section class="inspect-block"><h3>03 · 主会话收到的返回通知</h3><p class="intro">返回通知来自父 Session；它不是 child 的最后助手消息，也不是验收结论。</p>${notificationBody(notification) ? `<div class="quote" style="max-height:180px;overflow:auto;white-space:pre-wrap">${esc(notificationBody(notification))}</div>` : '<p class="intro">通知正文尚未提取；可打开来源查看，不代表没有返回内容。</p>'}${evidenceLink(notification, '打开父侧返回通知')}</section><section class="inspect-block"><h3>04 · 证据与缺口</h3>${item.dispatches.map((entry, index) => evidenceLink(entry.event, `${entry.event.native?.tool === 'send_input' ? '后续指令' : '派发要求'} ${index + 1} · 查看原文`)).join('')}<div class="boundary" style="margin-top:8px">${esc(childBoundary)}</div><p class="intro" style="margin-top:9px">派发次数：${esc(item.dispatches.length)} · Agent ID：${esc(C.compactId(agent.agent_id))} · 父级：${esc(C.compactId(agent.parent_agent_id))}</p></section></div>`;
  }

  function card(item, selected) {
    return `<button class="c-reuse-card ${selected ? 'selected' : ''}" data-c-agent="${esc(item.agent.agent_id)}"><span class="topline"><strong>${esc(item.agent.nickname || 'UNKNOWN')}</strong><span class="pill purple" style="margin-left:auto">角色线索 · 待整理</span></span><span class="task">${esc(item.task.title)}</span><span class="desc">${esc(item.task.summary)}</span><span class="card-bottom"><span class="pill blue">真实派发</span><span class="pill">${esc(item.dispatches.length)} 次</span><span class="spacer"></span><small>查看 →</small></span></button>`;
  }

  function renderRail(model) {
    const rail = document.querySelector('.railscroll');
    if (!rail) return;
    const representatives = representativeSet(model);
    const repIds = new Set(representatives.map(item => item.agent.agent_id));
    const identityCount = model.root ? model.childCount + 1 : model.childCount;
    const queryText = String(state.cFilter || '').trim().toLowerCase();
    const matches = item => !queryText || [item.agent.nickname, item.task.title, item.task.summary, item.task.role].join(' ').toLowerCase().includes(queryText);
    const known = representatives.filter(matches);
    const other = model.all.filter(item => !repIds.has(item.agent.agent_id) && matches(item));
    const hiddenCount = model.all.length - representatives.length;
    rail.innerHTML = `<div class="c-reuse-rail-label">导航</div><button class="navitem ${state.cView !== 'lineage' ? 'active' : ''}" data-c-view="map"><span>⌗</span><span class="t"><strong>任务分工地图</strong><br><small>代表任务 · ${identityCount} 个身份</small></span></button><button class="navitem ${state.cView === 'lineage' ? 'active' : ''}" data-c-view="lineage"><span>⑂</span><span class="t"><strong>原生 Agent 血缘</strong><br><small>1 Root · ${model.childCount} Child</small></span></button><div class="c-reuse-rail-label">代表任务 <span class="pill blue">${representatives.length}</span></div><div id="c-known-list">${known.map(item => `<button class="c-reuse-rail-item ${item.agent.agent_id === state.selectedAgent ? 'selected' : ''}" data-c-agent="${esc(item.agent.agent_id)}"><strong>${esc(item.agent.nickname || 'Agent')}</strong><small>${esc(item.task.title)}</small></button>`).join('') || '<div class="c-reuse-rail-item">没有匹配的代表任务</div>'}</div><details class="c-reuse-rail-more" ${queryText ? 'open' : ''}><summary>其他 ${hiddenCount} 个已知任务 <span class="pill">有派发正文</span></summary><div class="rail-more-note">这些身份也有真实派发内容，但没有全部挤进首屏地图。点击后在右侧查看同样的任务说明和父侧证据。</div><div id="c-other-list">${other.map(item => `<button class="c-reuse-rail-item ${item.agent.agent_id === state.selectedAgent ? 'selected' : ''}" data-c-agent="${esc(item.agent.agent_id)}"><strong>${esc(item.agent.nickname || 'Agent')}</strong><small>${esc(item.task.title)}</small></button>`).join('') || '<div class="c-reuse-rail-item">没有匹配的任务</div>'}</div></details><div id="sessionList" style="display:none"></div>`;
    const search = $('#search');
    if (search) {
      search.placeholder = '搜索 Agent / 任务内容';
      if (!search.dataset.cReuseBound) {
        search.dataset.cReuseBound = '1';
        search.addEventListener('input', event => { state.cFilter = event.target.value; renderC(); });
      }
      search.value = state.cFilter || '';
    }
    const foot = document.querySelector('.railfoot');
    if (foot) foot.innerHTML = '来源：父 Session 的本地 JSONL。<br>任务说明来自派发正文；父侧返回通知单独标记，child 内部记录保持缺口。';
  }

  function mapMarkup(model) {
    const reps = representativeSet(model);
    const edgePaths = '<path d="M610 190 C610 230 205 210 205 251"/><path d="M610 190 L610 251"/><path d="M610 190 C610 225 990 213 990 251"/>';
    const zone = (key, title, description, color, left, width) => {
      const items = reps.filter(candidate => groupForRole(candidate.task.role) === key);
      const count = items.length;
      return `<section class="c-reuse-zone ${key}" style="left:${left}px;width:${width}px"><div class="zone-title"><i class="c-reuse-dot ${color}"></i><h3>${esc(title)}</h3><span class="zone-count">${count} 个任务</span></div><p class="zone-sub">${esc(description)}</p>${items.length ? items.map(item => card(item, item.agent.agent_id === state.selectedAgent)).join('') : '<div class="boundary">当前没有符合这一区域的派发内容。</div>'}<div class="zone-foot">暂按派发角色归类，不是完整任务解释</div></section>`;
    };
    const otherCount = Math.max(0, model.all.length - reps.length);
    return `<div class="c-reuse-viewport"><div class="c-reuse-stage"><svg class="c-reuse-edges" viewBox="0 0 1220 810" aria-hidden="true" stroke="#a8c4d2" stroke-width="2" fill="none" stroke-dasharray="5 6"><g>${edgePaths}</g><g fill="#85afbf" stroke="none"><circle cx="205" cy="250" r="4"/><circle cx="610" cy="250" r="4"/><circle cx="990" cy="250" r="4"/></g></svg><button class="c-reuse-root ${!state.selectedAgent || state.selectedAgent === model.root?.agent_id ? 'selected' : ''}" data-c-agent="${esc(model.root?.agent_id || state.sessionId)}"><span class="pill blue">ROOT · NATIVE</span><h3>Root Session / 主执行体</h3><p>真实父 Session 负责派发；这里不把父侧最终消息冒充整个运行结果。</p><div class="meta"><span class="pill">${esc(model.childCount)} 个 child Agent</span><span class="pill purple">${esc(model.dispatchCount)} 个有派发正文的执行者</span></div></button>${zone('research','研究与证据收集','派发内容明确要求研究、资料搜集或参考系统初选。','research',62,350)}${zone('audit','治理审阅','派发内容明确要求独立审阅、框架审计或意图核对。','audit',438,352)}${zone('delivery','授权文档写入','只显示派发正文明确支持的受限文档或产出任务。','delivery',817,348)}<div class="c-reuse-unknown"><div><span class="pill amber">OTHER · NATIVE DISPATCH</span><h3>${esc(otherCount)} 个其他已知任务</h3><p>这些身份同样有真实派发正文；没有把它们硬塞进三类区域。通过左侧“其他已知任务”逐一查看。</p></div><button type="button" data-c-view="lineage">查看全部身份 →</button></div></div></div><div class="c-reuse-hint"><span>◎</span><span>保持空间阅读位置<br><small>拖动画布 · 滚轮缩放 · 点击选择</small></span></div><div class="c-reuse-zoom"><button type="button" data-c-zoom="out" title="缩小">−</button><button type="button" data-c-zoom="in" title="放大">＋</button><button type="button" data-c-zoom="fit" title="适配">⌗</button></div>`;
  }

  function groupForRole(role) {
    if (role === 'AFK research worker' || role === 'DSH Research Worker') return 'research';
    if (['DSH Global Reviewer', 'Codex Local Auditor', 'Blind Frame Auditor', 'Retrospective Frame Auditor', 'Blind Intent Fidelity Auditor', 'Governance v2 Global Reviewer', 'Local Audit Repair Verifier'].includes(role)) return 'audit';
    if (role === 'DSH Scribe') return 'delivery';
    return 'other';
  }

  function lineageMarkup(model) {
    const agents = [model.root, ...model.all.map(item => item.agent)].filter(Boolean);
    return `<div class="c-reuse-lineage"><div class="c-reuse-lineage-head"><div><span class="cap">AGENTS / NATIVE LINEAGE</span><h2>Root → ${esc(model.childCount)} 个直属 Agent</h2><p>这里核对真实身份和父子关系；任务说明仍以派发正文为准。</p></div><button class="btn" data-c-view="map">返回任务地图 →</button></div>${agents.map(agent => { const item = model.all.find(candidate => candidate.agent.agent_id === agent.agent_id); const isRoot = !item; return `<button class="c-reuse-lineage-row ${agent.agent_id === state.selectedAgent ? 'selected' : ''}" data-c-agent="${esc(agent.agent_id)}"><span class="time">${isRoot ? 'ROOT' : 'CHILD'}</span><strong>${esc(agent.nickname || 'Root Session')}</strong><span class="preview">${isRoot ? '父 Session 身份与派发总览' : esc(item?.task.title || '待分类任务')}</span><span class="status">${isRoot ? 'NATIVE' : `${item?.dispatches.length || 0} 次派发`}</span></button>`; }).join('')}</div>`;
  }

  function fitCanvas() {
    const map = document.querySelector('.c-reuse-map');
    if (!map) return;
    const width = map.clientWidth;
    const height = map.clientHeight;
    const z = Math.max(.34, Math.min(.91, (width - 38) / 1220, (height - 30) / 810));
    state.cTransform = { z, x: (width - 1220 * z) / 2, y: (height - 810 * z) / 2 };
    applyTransform();
  }

  function applyTransform() {
    const stage = document.querySelector('.c-reuse-stage');
    const transform = state.cTransform || { x: 0, y: 0, z: 1 };
    if (stage) stage.style.transform = `translate(${transform.x}px,${transform.y}px) scale(${transform.z})`;
  }

  function zoomCanvas(factor, cx, cy) {
    const map = document.querySelector('.c-reuse-map');
    if (!map) return;
    const before = state.cTransform || { x: 0, y: 0, z: 1 };
    const next = Math.max(.33, Math.min(1.65, before.z * factor));
    const rect = map.getBoundingClientRect();
    const px = Number.isFinite(cx) ? cx - rect.left : rect.width / 2;
    const py = Number.isFinite(cy) ? cy - rect.top : rect.height / 2;
    const ratio = next / before.z;
    state.cTransform = { z: next, x: px - (px - before.x) * ratio, y: py - (py - before.y) * ratio };
    applyTransform();
  }

  function bindCanvas() {
    const viewport = document.querySelector('.c-reuse-viewport');
    if (!viewport) return;
    if (!state.cTransform) fitCanvas(); else applyTransform();
    document.querySelectorAll('[data-c-zoom]').forEach(button => button.addEventListener('click', () => {
      if (button.dataset.cZoom === 'fit') fitCanvas();
      else zoomCanvas(button.dataset.cZoom === 'in' ? 1.18 : 1 / 1.18);
    }));
    let drag = null;
    viewport.addEventListener('pointerdown', event => {
      if (event.target.closest('button')) return;
      const transform = state.cTransform || { x: 0, y: 0, z: 1 };
      drag = { x: event.clientX, y: event.clientY, ox: transform.x, oy: transform.y };
      viewport.setPointerCapture(event.pointerId);
      viewport.classList.add('grabbed');
    });
    viewport.addEventListener('pointermove', event => {
      if (!drag) return;
      state.cTransform = { ...(state.cTransform || { z: 1 }), x: drag.ox + event.clientX - drag.x, y: drag.oy + event.clientY - drag.y };
      applyTransform();
    });
    const release = () => { drag = null; viewport.classList.remove('grabbed'); };
    viewport.addEventListener('pointerup', release);
    viewport.addEventListener('pointercancel', release);
    viewport.addEventListener('wheel', event => {
      event.preventDefault();
      zoomCanvas(event.deltaY < 0 ? 1.08 : 1 / 1.08, event.clientX, event.clientY);
    }, { passive: false });
  }

  function renderCHeader(model) {
    const lineage = state.cView === 'lineage';
    const identityCount = model.root ? model.childCount + 1 : model.childCount;
    $('#eyebrow').textContent = lineage ? 'AGENTS / NATIVE LINEAGE' : 'AGENTS / COGNITIVE MAP';
    $('#title').textContent = lineage ? `Root → ${model.childCount} 个直属 Agent` : '谁被真实派去做什么？';
    $('#subtitle').textContent = lineage ? '身份和父子关系来自父 Session；不把工具调用或返回通知提升为 child 执行结果。' : '把真实派发任务放在第一眼；需要时再打开父侧派发和返回通知。';
    $('.toolbar').innerHTML = `<span class="pill blue">${esc(identityCount)} native identities</span><button class="btn" data-c-top-fit="1">⌗ 适配</button><button class="btn" data-c-view="lineage">⑂ 血缘</button>`;
  }

  function renderC() {
    if (!state.session) return;
    if (!(state.session.agents || []).some(agent => agent.parent_agent_id)) {
      const rail = document.querySelector('.railscroll');
      rail.innerHTML = '<div class="c-reuse-rail-label">当前 Session</div><p style="padding:12px">执行步骤图：请求 → 轮次 → 工具操作。这里没有子 Agent，步骤不代表派发血缘。</p><div id="sessionList"></div>';
      $('.toolbar').innerHTML = '<span class="pill blue">1 个 Session · 无子 Agent</span>';
      return renderExecutionSteps();
    }
    const model = C.build(state.session);
    if (!state.cView) state.cView = 'map';
    if (!state.selectedAgent || (![model.root?.agent_id, ...model.all.map(item => item.agent.agent_id)].includes(state.selectedAgent))) state.selectedAgent = model.root?.agent_id || model.all[0]?.agent.agent_id || null;
    renderRail(model);
    renderCHeader(model);
    const item = selectedItem(model);
    const inspector = item ? childInspector(item) : rootInspector(model);
    const surface = state.cView === 'lineage' ? lineageMarkup(model) : `<div class="c-reuse-map">${mapMarkup(model)}</div>`;
    $('#body').innerHTML = `<div class="c-reuse-surface">${surface}<aside class="c-reuse-inspector">${inspector}</aside></div>`;
    bindCanvas();
  }

  document.addEventListener('click', event => {
    const agentButton = event.target.closest('[data-c-agent]');
    if (agentButton) {
      state.selectedAgent = agentButton.dataset.cAgent;
      const params = new URLSearchParams(location.search);
      params.set('tab', 'agents');
      params.set('session_id', state.sessionId);
      params.set('agent_id', state.selectedAgent);
      history.replaceState({}, '', `?${params.toString()}`);
      renderC();
      return;
    }
    const viewButton = event.target.closest('[data-c-view]');
    if (viewButton) {
      state.cView = viewButton.dataset.cView;
      renderC();
      return;
    }
    const evidenceButton = event.target.closest('[data-c-event]');
    if (evidenceButton) {
      const record = (state.session?.events || []).find(item => item.event_id === evidenceButton.dataset.cEvent);
      if (record) {
        evidenceTrigger = evidenceButton;
        openRecord(record);
        $('#modalTitle').textContent = `${record.kind === 'user' ? '父侧返回通知' : '父侧派发依据'} · 第 ${record.ordinal || record.evidence_ref?.line || '?'} 行`;
        $('#modalClose').focus();
      }
      return;
    }
    if (event.target.closest('#modalClose') || event.target.id === 'modal') closeEvidence();
    if (event.target.closest('[data-c-top-fit]')) fitCanvas();
  });

  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && $('#modal').classList.contains('open')) closeEvidence();
  });

  setTab = function (tab) {
    state.tab = tab;
    const params = new URLSearchParams(location.search);
    params.set('tab', tab);
    params.set('session_id', state.sessionId);
    if (tab === 'agents' && state.selectedAgent) params.set('agent_id', state.selectedAgent);
    else params.delete('agent_id');
    history.pushState({}, '', `?${params.toString()}`);
    render();
  };
  agents = renderC;
}());
