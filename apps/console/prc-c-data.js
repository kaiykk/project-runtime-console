(function () {
  const ROLE_GROUPS = [
    {
      key: 'research',
      title: '研究与证据收集',
      description: '派发内容明确要求研究、资料搜集或参考系统初选。',
      roles: ['AFK research worker', 'DSH Research Worker']
    },
    {
      key: 'audit',
      title: '治理审阅',
      description: '派发内容明确要求独立审阅、框架审计或意图核对。',
      roles: ['DSH Global Reviewer', 'Codex Local Auditor', 'Blind Frame Auditor', 'Retrospective Frame Auditor', 'Blind Intent Fidelity Auditor', 'Governance v2 Global Reviewer', 'Local Audit Repair Verifier']
    },
    {
      key: 'delivery',
      title: '授权文档写入',
      description: '派发内容明确要求受限范围内的文档或任务产出。',
      roles: ['DSH Scribe']
    }
  ];

  function compactId(value) {
    const text = String(value || '');
    return text.length > 8 ? `${text.slice(0, 8)}...${text.slice(-4)}` : text;
  }

  function firstLine(value) {
    return String(value || '').replace(/\s+/g, ' ').trim().split(/(?<=[.!?。！？])\s+/)[0] || '';
  }

  function normalizePrompt(value) {
    return String(value || '').replace(/\s+/g, ' ').trim();
  }

  function roleFor(prompt) {
    const text = normalizePrompt(prompt);
    const known = [
      ['AFK research worker', 'AFK research worker'],
      ['DSH Research Worker', 'DSH Research Worker'],
      ['DSH Global Reviewer', 'DSH Global Reviewer'],
      ['DSH Worker', 'DSH Worker'],
      ['DSH Scribe', 'DSH Scribe'],
      ['Blind Frame Auditor', 'Blind Frame Auditor'],
      ['Retrospective Frame Auditor', 'Retrospective Frame Auditor'],
      ['Blind Intent Fidelity Auditor', 'Blind Intent Fidelity Auditor'],
      ['Governance v2 Global Reviewer', 'Governance v2 Global Reviewer'],
      ['Local Audit Repair Verifier', 'Local Audit Repair Verifier'],
      ['fresh Codex Local Auditor', 'Codex Local Auditor']
    ];
    return (known.find(([needle]) => text.includes(needle)) || [null, null])[1];
  }

  function groupFor(role) {
    return ROLE_GROUPS.find(group => group.roles.includes(role)) || null;
  }

  function taskCopy(agent, dispatch) {
    const role = roleFor(dispatch.prompt);
    const source = normalizePrompt(dispatch.prompt);
    const titleByRole = {
      'AFK research worker': '调研指定问题的外部证据',
      'DSH Research Worker': '开展限定范围的研究工作',
      'DSH Global Reviewer': '独立审阅本轮边界与证据',
      'DSH Worker': '完成指定的受限任务包',
      'DSH Scribe': '记录已授权的规范更新',
      'Codex Local Auditor': '独立核对限定范围的任务结果',
      'Blind Frame Auditor': '独立检查研究框架',
      'Retrospective Frame Auditor': '回顾性检查已有框架材料',
      'Blind Intent Fidelity Auditor': '独立核对产物是否忠于原意',
      'Governance v2 Global Reviewer': '独立审阅治理收口材料',
      'Local Audit Repair Verifier': '核对审阅修复是否覆盖限定问题'
    };
    return {
      role,
      title: role ? `角色线索：${titleByRole[role]}` : '任务说明待整理',
      summary: '当前仅识别角色线索；具体任务、变化与结果尚未整理，请展开派发依据。',
      purpose: '派发原文没有用独立字段明确写出；这里不补造目的。',
      limits: '以派发原文为准；本页不把任务要求写成已完成结果。',
      deliverable: '以派发原文为准，展开“查看派发依据”核对。',
      source
    };
  }

  function dispatchEvents(session) {
    return (session.events || []).filter(event => event.kind === 'agent_event'
      && ['spawn_agent', 'send_input'].includes(event.native?.tool)
      && (event.native?.receiver_agents?.length > 0 || event.native?.id)
      && String(event.native?.prompt || '').trim());
  }

  function notificationsByAgent(session) {
    const notifications = new Map();
    (session.events || []).filter(event => event.kind === 'user'
      && String(event.content || '').includes('<subagent_notification>')).forEach(event => {
      const match = String(event.content || '').match(/agent_path\\?"?:\\?"([^"\\]+)\\?"?/);
      if (match && !notifications.has(match[1])) notifications.set(match[1], event);
    });
    return notifications;
  }

  function build(session) {
    const agentById = new Map((session.agents || []).map(agent => [agent.agent_id, agent]));
    const notifications = notificationsByAgent(session);
    const byAgent = new Map();
    dispatchEvents(session).forEach(event => {
      (event.native.receiver_agents || [{ thread_id: event.native.id }]).forEach(receiver => {
        const agent = agentById.get(receiver.thread_id);
        if (!agent) return;
        const item = byAgent.get(agent.agent_id) || {
          agent,
          dispatches: [],
          task: taskCopy(agent, event.native),
          notification: notifications.get(agent.agent_id) || null
        };
        const key = `${agent.agent_id}:${event.occurrence_id || event.event_id || event.call_id || event.ordinal}`;
        if (!item.dispatches.some(dispatch => dispatch.key === key)) item.dispatches.push({ key, event });
        byAgent.set(agent.agent_id, item);
      });
    });
    const items = [...byAgent.values()].map(item => ({
      ...item,
      dispatch: item.dispatches[0]?.event || null
    }));
    const groups = ROLE_GROUPS.map(group => ({
      ...group,
      items: items.filter(item => group.roles.includes(item.task.role))
    }));
    const classified = new Set(groups.flatMap(group => group.items.map(item => item.agent.agent_id)));
    const identityOnly = (session.agents || []).filter(agent => agent.parent_agent_id && !byAgent.has(agent.agent_id)).map(agent => ({
      agent,
      dispatches: [],
      task: {
        role: null,
        title: '待分类任务',
        summary: '身份已确认，但当前父侧投影没有可读取的派发正文。',
        purpose: '未知；不根据名字、ID 或调用数量补造。',
        limits: '保持为 UNKNOWN，等待可核对的派发证据。',
        deliverable: '未知；当前没有可确认的要求。'
      },
      notification: notifications.get(agent.agent_id) || null
    }));
    return {
      root: (session.agents || []).find(agent => !agent.parent_agent_id) || null,
      groups,
      other: [...items.filter(item => !classified.has(item.agent.agent_id)), ...identityOnly],
      all: [...items, ...identityOnly],
      childCount: (session.lineage?.child_count || 0),
      dispatchCount: items.length,
      notificationCount: notifications.size
    };
  }

  window.PrcCData = { build, compactId, normalizePrompt };
}());
