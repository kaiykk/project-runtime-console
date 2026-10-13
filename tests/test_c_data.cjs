// Portable adapter regression checks: no private transcripts or browser dependencies.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const context = { window: {} };
vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../apps/console/prc-c-data.js'), 'utf8'), context);
const build = context.window.PrcCData.build;
const event = (id, tool, prompt, target) => ({ event_id: id, kind: 'agent_event', native: { tool, prompt, ...target } });
const session = {
  agents: [{ agent_id: 'root' }, { agent_id: 'child', parent_agent_id: 'root', nickname: 'Example' }],
  lineage: { child_count: 1 },
  events: [event('spawn', 'spawn_agent', 'AFK research worker: read public docs', { receiver_agents: [{ thread_id: 'child' }] }),
    event('followup', 'send_input', 'Only public evidence', { id: 'child' }),
    event('wait', 'wait', 'not a task', { receiver_agents: [{ thread_id: 'child' }] })]
};
const model = build(session);
assert.equal(model.all.length, 1);
assert.equal(model.all[0].dispatches.length, 2);
assert.equal(model.all[0].dispatches[1].event.event_id, 'followup');
assert.match(model.all[0].task.summary, /尚未整理/);
assert.equal(build({ agents: [], events: [] }).all.length, 0);
console.log('PASS: identity association, followup retention, wait exclusion and provisional role claims');
