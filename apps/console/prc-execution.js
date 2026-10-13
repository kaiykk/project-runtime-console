/* Delivery point A: the Agents surface is a truthful runtime map, not a task board. */
(function () {
  function turnEvents(turn, data) {
    return (data.events || []).filter(event => Array.isArray(turn.event_ids)
      ? turn.event_ids.includes(event.event_id)
      : turn.turn_occurrence_id ? event.turn_occurrence_id === turn.turn_occurrence_id
      : event.turn_id === turn.turn_id);
  }

  function firstTool(turn, data) {
    return turnEvents(turn, data).find(event => event.kind === 'tool_call');
  }

  function turnSummary(turn, data) {
    const event = turnEvents(turn, data).find(item => item.kind === 'user' || item.kind === 'assistant');
    return event ? excerpt(textOf(event), 150) : '这一轮没有可读取的用户或助手正文。';
  }

  function locatorText(locator) {
    if (!locator) return '证据定位不可用';
    return `原始记录第 ${locator.line || '?'} 行 · byte ${locator.byte_offset ?? '?'} · ${locator.locator_kind || 'record'}`;
  }

  function mapShell(stageHtml, stageHeight, inspectorHtml, legend) {
    return `<main class="runtime-map"><div class="runtime-viewport" id="runtimeViewport"><div class="runtime-stage" id="runtimeStage" style="height:${stageHeight}px">${stageHtml}</div></div><div class="runtime-legend">${legend}</div><div class="zoom runtime-zoom" role="toolbar" aria-label="Agents 画布操作"><button data-runtime-zoom="out" title="缩小" aria-label="缩小">−</button><button data-runtime-zoom="in" title="放大" aria-label="放大">＋</button><button data-runtime-zoom="fit" title="适应窗口" aria-label="适应窗口">⌗</button></div></main><aside class="focuspanel runtime-inspector">${inspectorHtml}</aside>`;
  }

  function bindRuntimeCanvas(stageHeight) {
    const viewport = $('#runtimeViewport');
    const stage = $('#runtimeStage');
    const map = $('.runtime-map');
    if (!viewport || !stage || !map) return;
    const view = state.executionTransform || { x: 0, y: 0, z: 1 };
    const clamp = value => Math.max(.45, Math.min(1.5, value));
    const transform = () => { state.executionTransform = view; stage.style.transform = `translate(${view.x}px,${view.y}px) scale(${view.z})`; };
    const fit = () => {
      const width = map.clientWidth;
      const height = map.clientHeight;
      view.z = clamp(Math.min((width - 24) / 1220, (height - 24) / stageHeight, 1));
      view.x = (width - 1220 * view.z) / 2;
      view.y = Math.max(12, (height - stageHeight * view.z) / 2);
      transform();
    };
    const zoom = (factor, cx, cy) => {
      const old = view.z;
      const next = clamp(old * factor);
      if (next === old) return;
      if (Number.isFinite(cx) && Number.isFinite(cy)) {
        const scale = next / old;
        view.x = cx - (cx - view.x) * scale;
        view.y = cy - (cy - view.y) * scale;
      }
      view.z = next;
      transform();
    };
    if (state.executionTransform) transform(); else fit();
    $$('[data-runtime-zoom]').forEach(button => button.addEventListener('click', () => {
      const action = button.dataset.runtimeZoom;
      if (action === 'fit') fit();
      else zoom(action === 'in' ? 1.18 : .85);
    }));
    let drag = null;
    viewport.addEventListener('pointerdown', event => {
      if (event.target.closest('button')) return;
      drag = { x: event.clientX, y: event.clientY, ox: view.x, oy: view.y };
      viewport.setPointerCapture(event.pointerId);
      viewport.classList.add('grabbed');
    });
    viewport.addEventListener('pointermove', event => {
      if (!drag) return;
      view.x = drag.ox + event.clientX - drag.x;
      view.y = drag.oy + event.clientY - drag.y;
      transform();
    });
    const release = () => { drag = null; viewport.classList.remove('grabbed'); };
    viewport.addEventListener('pointerup', release);
    viewport.addEventListener('pointercancel', release);
    viewport.addEventListener('wheel', event => {
      event.preventDefault();
      const rect = map.getBoundingClientRect();
      zoom(event.deltaY < 0 ? 1.08 : .92, event.clientX - rect.left, event.clientY - rect.top);
    }, { passive: false });
  }

  function evidenceButton(event, label) {
    if (!event) return '<div class="unknown">这一处没有可打开的原始记录。</div>';
    return `<button class="evidence-row" data-event="${esc(event.event_id)}"><b>${esc(label || event.event_type || event.kind)}</b><small>${esc(locatorText(event.evidence_ref))} · 点击查看原文</small></button>`;
  }

  function stepInspector(turn, data) {
    const events = turnEvents(turn, data);
    const firstMessage = events.find(event => event.kind === 'user' || event.kind === 'assistant');
    return `<div class="focushead"><div class="eyebrow">FOCUS INSPECTOR <span class="pill blue">TURN ${esc(turn.index)}</span></div><h2>执行轮次 ${esc(turn.index)}</h2><p>Turn 是一次执行轮次，不是 Agent 身份。</p></div><div class="focusscroll"><div class="block"><h3>01 · 这一轮发生了什么</h3><div class="quote">${esc(excerpt(textOf(firstMessage), 220) || '没有可读取的用户或助手正文。')}</div><p style="margin-top:9px;color:#8499a5;font-size:10px">共 ${esc(events.length)} 条真实记录。页面只按 Turn 包含关系组织它们。</p></div><div class="block"><h3>02 · 这轮里的真实记录</h3>${events.slice(0, 12).map(event => evidenceButton(event, `${event.event_type} · ${event.kind}`)).join('') || '<div class="unknown">本轮没有可展示的记录。</div>'}${events.length > 12 ? `<div class="unknown">其余 ${events.length - 12} 条仍保留在原始 Session；当前只显示前 12 条可打开记录。</div>` : ''}</div><div class="block"><h3>03 · 工具记录边界</h3><div class="unknown">工具按钮只打开原始记录；它不代表工具导致了某个结论，也不代表本轮已经完成。</div></div></div>`;
  }

  function renderWithoutLineage(data) {
    const turns = state.session?.turns || [];
    const selectedTurn = turns.find(turn => turn.turn_id === state.selectedTurn);
    const columns = turns.map((turn, index) => ({ turn, index }));
    const centers = columns.map((_, index) => 176 + index * 217);
    const edges = centers.map((center, index) => { const turn = turns[index]; const tool = firstTool(turn, data); const toolY = 410; return `<path d="M610 190 C610 220 ${center} 218 ${center} 250"/><circle cx="${center}" cy="250" r="4"/>${tool ? `<path d="M${center} 381 L${center} ${toolY}"/><circle cx="${center}" cy="${toolY}" r="3"/>` : ''}`; }).join('');
    const cards = columns.map(({ turn, index }) => { const events = turnEvents(turn, data); const tool = firstTool(turn, data); return `<section class="step-column"><h3>执行轮次 ${esc(turn.index)}</h3><p>这一栏只表示 Turn 包含的真实记录 · ${events.length} 条</p><button class="step-turn ${selectedTurn?.turn_id === turn.turn_id ? 'selected' : ''}" data-turn="${esc(turn.turn_id)}"><strong>Turn ${esc(turn.index)}</strong><span class="step-summary">${esc(turnSummary(turn, data))}</span><small>${esc(turn.started_at || '时间未提供')} · 点击看详情</small></button>${tool ? `<button class="step-tool" data-event="${esc(tool.event_id)}"><strong>真实工具操作</strong><span>${esc(tool.tool_name || tool.event_type || 'UNKNOWN TOOL')} · 第 ${esc(tool.ordinal)} 行</span></button>` : '<div class="step-unavailable">本轮没有可确认的工具调用。</div>'}</section>`; }).join('');
    const rootHtml = `<button class="runtime-root ${!selectedTurn ? 'selected' : ''}" data-runtime-root="1"><span class="pill amber">SESSION · IDENTITY ONLY</span><h3>Session / 当前执行记录</h3><p>没有可确认的 child Agent lineage；下面只显示 Turn 和真实工具记录。</p><div class="runtime-meta"><span class="pill">${esc(turns.length)} 个 Turn</span><span class="pill">${esc(state.session?.summary?.event_count || 0)} 条记录</span><span class="pill amber">NO_NATIVE_AGENT_LINEAGE</span></div></button>`;
    const stageHtml = `<svg class="runtime-edges" viewBox="0 0 1220 900" aria-hidden="true">${edges}</svg>${rootHtml}<div class="step-columns">${cards}</div><div class="runtime-boundary" style="top:815px"><span class="pill amber">步骤关系</span><div><h3>这张图表示什么</h3><p>实线只表示“Session 包含 Turn、Turn 中有记录”。它不表示 Agent 血缘，也不表示工具导致了某个结论；未知归属会明确保留为 UNKNOWN。</p></div></div>`;
    $('#eyebrow').textContent = 'AGENTS / SESSION EXECUTION STEPS';
    $('#title').textContent = '这个 Session 实际执行了哪些步骤？';
    $('#subtitle').textContent = '没有 child Agent 时，页面仍然展示真实 Turn、工具操作和原始证据，不制造 Agent 身份。';
    $('#body').innerHTML = mapShell(stageHtml, 900, selectedTurn ? stepInspector(selectedTurn, data) : `<div class="focushead"><div class="eyebrow">FOCUS INSPECTOR <span class="pill amber">SESSION ONLY</span></div><h2>先选择一个执行轮次</h2><p>这里没有 Agent 卡片，只有 Session → Turn → 真实记录。</p></div><div class="focusscroll"><div class="block"><h3>01 · 真实边界</h3><p>源文件确认 ${esc(turns.length)} 个 Turn、${esc(state.session?.summary?.tool_call_count || 0)} 次工具调用、${esc(state.session?.summary?.event_count || 0)} 条记录。</p><div class="unknown">NO_NATIVE_AGENT_LINEAGE：不能从普通工具调用推断 child Agent。</div></div><div class="block"><h3>02 · 未分配记录</h3><p>${esc(state.session?.summary?.unassigned_event_count || 0)} 条记录位于明确的来源边界，页面不会猜它们属于哪一轮。</p></div><button class="btn primary" data-tab="trace">进入 Trace 查看全部记录</button></div>` , '实线 = Session 包含 Turn · Turn 下的工具按钮 = 真实 tool_call · 不表示因果关系');
    bindRuntimeCanvas(900);
    $$('[data-runtime-root]').forEach(button => button.addEventListener('click', () => { state.selectedTurn = null; renderWithoutLineage(agentData()); }));
    $$('[data-turn]').forEach(button => button.addEventListener('click', () => { state.selectedTurn = button.dataset.turn; state.selectedAgent = null; renderWithoutLineage(agentData()); }));
    $$('[data-event]').forEach(button => button.addEventListener('click', () => openRecord(data.events.find(event => event.event_id === button.dataset.event))));
  }

  function renderRuntimeAgents() {
    const data = agentData();
    if ((data.agents || []).some(agent => agent.parent_agent_id)) {
      $('#body').innerHTML = '<div class="empty"><h3>任务地图加载失败</h3><p>请刷新页面；不会回退到已废弃的身份卡片墙。</p></div>';
      return;
    }
    renderWithoutLineage(data);
  }

  agents = renderRuntimeAgents;
}());
