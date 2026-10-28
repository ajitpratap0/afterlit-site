'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const script = fs.readFileSync(path.resolve(__dirname, '../site.js'), 'utf8');

function element(extra = {}) {
  const listeners = new Map();
  const attributes = new Map();
  return {
    textContent: '',
    className: '',
    classList: (() => { const set = new Set(); return { add(n) { set.add(n); }, remove(n) { set.delete(n); }, toggle(n, on) { if (on) set.add(n); else set.delete(n); }, contains(n) { return set.has(n); } }; })(),
    ...extra,
    addEventListener(name, callback) { listeners.set(name, callback); },
    setAttribute(name, value) { attributes.set(name, value); },
    getAttribute(name) { return attributes.get(name); },
    removeAttribute(name) { attributes.delete(name); },
    fire(name) { assert.ok(listeners.has(name), `missing ${name} listener`); listeners.get(name)(); },
  };
}

function workbench(missing, extra = {}) {
  const nodes = {
    '#demo-controls': element({ disabled: true }),
    '#brightness': element({ value: '75' }),
    '#demo-lamp': element({ className: 'demo-lamp level-75 tone-warm' }),
    '#brightness-value': element({ value: '75%' }),
    '#req-power': element({ textContent: 'On' }),
    '#req-level': element({ textContent: '75%' }),
    '#req-color': element({ textContent: 'Warm white' }),
    '#state-power': element({ textContent: 'On' }),
    '#state-level': element({ textContent: '75%' }),
    '#state-color': element({ textContent: 'Warm white' }),
    '#color-off-note': element({ hidden: true }),
    '.swatches': element(),
    ...extra,
  };
  const swatches = ['warm', 'amber', 'sage', 'blue'].map((tone) => element({ dataset: { tone }, disabled: false }));
  const classes = new Set();
  const document = {
    querySelector(selector) { return selector === missing ? null : nodes[selector]; },
    querySelectorAll(selector) { return selector === '.swatch' ? swatches : []; },
    documentElement: { classList: { add(name) { classes.add(name); } } },
  };
  vm.runInNewContext(script, { document }, { timeout: 1000, filename: 'site.js' });
  return { nodes, swatches, classes };
}

test('enables the simulation and reflects brightness at off and full', () => {
  const { nodes, classes } = workbench();
  assert.equal(nodes['#demo-controls'].disabled, false);
  assert.ok(classes.has('js-ready'));
  assert.equal(nodes['#brightness'].getAttribute('aria-valuetext'), '75%');

  nodes['#brightness'].value = '0';
  nodes['#brightness'].fire('input');
  assert.equal(nodes['#brightness'].getAttribute('aria-valuetext'), 'Off');
  assert.equal(nodes['#state-power'].textContent, 'Off');
  assert.equal(nodes['#state-level'].textContent, '0%');
  assert.equal(nodes['#state-color'].textContent, 'None');
  assert.equal(nodes['#brightness-value'].textContent, '0%');
  assert.match(nodes['#demo-lamp'].className, /\blevel-0\b/);

  nodes['#brightness'].value = '100';
  nodes['#brightness'].fire('input');
  assert.equal(nodes['#brightness'].getAttribute('aria-valuetext'), '100%');
  assert.equal(nodes['#state-power'].textContent, 'On');
  assert.equal(nodes['#state-level'].textContent, '100%');
  assert.match(nodes['#demo-lamp'].className, /\blevel-100\b/);

  nodes['#brightness'].value = '25';
  nodes['#brightness'].fire('input');
  assert.equal(nodes['#brightness'].getAttribute('aria-valuetext'), '25%');
});

test('color selection updates readback and maintains one pressed swatch', () => {
  const { nodes, swatches } = workbench();
  swatches[3].fire('click');
  assert.equal(nodes['#state-color'].textContent, 'Blue');
  assert.match(nodes['#demo-lamp'].className, /\btone-blue\b/);
  assert.deepEqual(swatches.map((swatch) => swatch.getAttribute('aria-pressed')), [
    'false', 'false', 'false', 'true',
  ]);
  swatches[1].fire('click');
  assert.equal(nodes['#state-color'].textContent, 'Amber');
  assert.deepEqual(swatches.map((swatch) => swatch.getAttribute('aria-pressed')), [
    'false', 'true', 'false', 'false',
  ]);
});

test('missing required readback leaves controls disabled', () => {
  const { nodes, classes } = workbench('#state-power');
  assert.equal(nodes['#demo-controls'].disabled, true);
  assert.equal(classes.has('js-ready'), false);
});

function readbackNode() {
  const classes = new Set();
  const log = [];
  return {
    classes,
    log,
    offsetWidth: 0,
    classList: {
      add(name) { classes.add(name); log.push('add:' + name); },
      remove(name) { classes.delete(name); log.push('remove:' + name); },
    },
  };
}

test('readback confirmation plays only after user changes, never on load', () => {
  const readback = readbackNode();
  const { nodes, swatches } = workbench(undefined, { '.readback': readback });
  assert.equal(readback.classes.has('is-confirmed'), false);
  assert.deepEqual(readback.log, []);

  nodes['#brightness'].value = '50';
  nodes['#brightness'].fire('input');
  assert.equal(nodes['#state-level'].textContent, '50%');
  assert.ok(readback.classes.has('is-confirmed'));

  swatches[2].fire('click');
  assert.equal(nodes['#state-color'].textContent, 'Sage');
  assert.deepEqual(readback.log.slice(-2), ['remove:is-confirmed', 'add:is-confirmed']);
});

test('initial update does not rewrite unchanged readback text', () => {
  let writes = 0;
  const power = element();
  let text = 'On';
  Object.defineProperty(power, 'textContent', {
    get() { return text; },
    set(next) { writes += 1; text = next; },
  });
  const { nodes } = workbench(undefined, { '#state-power': power });
  assert.equal(writes, 0);
  nodes['#brightness'].value = '0';
  nodes['#brightness'].fire('input');
  assert.equal(writes, 1);
  assert.equal(text, 'Off');
});

test('inherited object keys are not accepted as tones', () => {
  const { nodes, swatches } = workbench();
  for (const key of ['__proto__', 'constructor', 'toString']) {
    swatches[0].dataset.tone = key;
    swatches[0].fire('click');
    assert.equal(nodes['#state-color'].textContent, 'Warm white');
    assert.match(nodes['#demo-lamp'].className, /\btone-warm\b/);
  }
});

test('requested and reported back update together in the same input', () => {
  const { nodes, swatches } = workbench();
  nodes['#brightness'].value = '50';
  nodes['#brightness'].fire('input');
  assert.equal(nodes['#req-level'].textContent, '50%');
  assert.equal(nodes['#state-level'].textContent, '50%');
  swatches[2].fire('click');
  assert.equal(nodes['#req-color'].textContent, 'Sage');
  assert.equal(nodes['#state-color'].textContent, 'Sage');
  for (const key of ['power', 'level', 'color']) {
    assert.equal(nodes['#req-' + key].textContent, nodes['#state-' + key].textContent);
  }
});

test('power off disables swatches and never reports a color', () => {
  const { nodes, swatches } = workbench();
  swatches[1].fire('click');
  nodes['#brightness'].value = '0';
  nodes['#brightness'].fire('input');
  assert.deepEqual(swatches.map((swatch) => swatch.disabled), [true, true, true, true]);
  assert.equal(nodes['#color-off-note'].hidden, false);
  assert.ok(nodes['#color-off-note'].classList.contains('is-shown'));
  assert.equal(nodes['.swatches'].getAttribute('aria-describedby'), 'color-off-note');
  assert.equal(nodes['#req-color'].textContent, 'None');
  assert.equal(nodes['#state-color'].textContent, 'None');
  assert.equal(nodes['#state-power'].textContent, 'Off');
  swatches[3].fire('click');
  assert.equal(nodes['#state-color'].textContent, 'None');
  assert.match(nodes['#demo-lamp'].className, /\btone-amber\b/);
  assert.equal(swatches[1].getAttribute('aria-pressed'), 'true');
  nodes['#brightness'].value = '25';
  nodes['#brightness'].fire('input');
  assert.deepEqual(swatches.map((swatch) => swatch.disabled), [false, false, false, false]);
  assert.equal(nodes['#color-off-note'].hidden, false);
  assert.ok(!nodes['#color-off-note'].classList.contains('is-shown'));
  assert.equal(nodes['.swatches'].getAttribute('aria-describedby'), undefined);
  assert.equal(nodes['#req-color'].textContent, 'Amber');
  assert.equal(nodes['#state-color'].textContent, 'Amber');
});

test('missing requested readback leaves controls disabled', () => {
  const { nodes, classes } = workbench('#req-level');
  assert.equal(nodes['#demo-controls'].disabled, true);
  assert.equal(classes.has('js-ready'), false);
});

test('initial update does not rewrite unchanged requested text', () => {
  let writes = 0;
  const requested = element();
  let text = 'Warm white';
  Object.defineProperty(requested, 'textContent', {
    get() { return text; },
    set(next) { writes += 1; text = next; },
  });
  workbench(undefined, { '#req-color': requested });
  assert.equal(writes, 0);
});

function classedElement(text) {
  const names = new Set();
  return element({
    textContent: text,
    classList: {
      add(name) { names.add(name); },
      remove(name) { names.delete(name); },
      contains(name) { return names.has(name); },
    },
  });
}

// New test. Swatch clicks are ignored while the lamp is off, and power off also rewrites Color to "None".
test('pencil stroke marks only values a user change rewrote, both steps together, never on load', () => {
  const readback = readbackNode();
  const reqColor = classedElement('Warm white');
  const power = classedElement('On');
  const level = classedElement('75%');
  const color = classedElement('Warm white');
  const { nodes, swatches } = workbench(undefined, {
    '.readback': readback, '#req-color': reqColor,
    '#state-power': power, '#state-level': level, '#state-color': color,
  });
  const fresh = () => [power, level, color].map((node) => node.classList.contains('is-fresh'));
  assert.deepEqual(fresh(), [false, false, false]);
  assert.equal(reqColor.classList.contains('is-fresh'), false);
  nodes['#brightness'].value = '50';
  nodes['#brightness'].fire('input');
  assert.deepEqual(fresh(), [false, true, false]);
  nodes['#brightness'].value = '0';
  nodes['#brightness'].fire('input');
  assert.equal(color.textContent, 'None');
  assert.deepEqual(fresh(), [true, true, true]);
  assert.equal(reqColor.classList.contains('is-fresh'), true);
  nodes['#brightness'].value = '50';
  nodes['#brightness'].fire('input');
  swatches[1].fire('click');
  assert.equal(color.textContent, 'Amber');
  assert.deepEqual(fresh(), [false, false, true]);
  assert.equal(reqColor.classList.contains('is-fresh'), true);
  // Re-selecting the current tone rewrites nothing, so the last record stays.
  swatches[1].fire('click');
  assert.deepEqual(fresh(), [false, false, true]);
});

test('a focused nav link is scrolled fully into view inside the phone nav row', () => {
  let handler;
  const nav = { addEventListener(name, callback) { if (name === 'focusin') handler = callback; } };
  const { nodes } = workbench(undefined, { '.site-header nav': nav });
  assert.equal(nodes['#demo-controls'].disabled, false);
  assert.equal(typeof handler, 'function');
  const calls = [];
  handler({ target: { scrollIntoView(options) { calls.push(options); } } });
  assert.equal(calls.length, 1);
  assert.equal(calls[0].block, 'nearest');
  assert.equal(calls[0].inline, 'nearest');
  handler({ target: null });
  handler(undefined);
  assert.equal(calls.length, 1);
});

test('the nav marks the section crossing the middle of the screen as the current location', () => {
  const makeLink = (href, offsetLeft) => {
    const attributes = new Map([['href', href]]);
    return {
      offsetLeft, offsetWidth: 80,
      getAttribute(name) { return attributes.get(name); },
      setAttribute(name, value) { attributes.set(name, value); },
      removeAttribute(name) { attributes.delete(name); },
    };
  };
  const links = [makeLink('#today', 0), makeLink('#check', 100), makeLink('#status', 300)];
  const nav = {
    scrollLeft: 0, scrollWidth: 500, clientWidth: 200,
    addEventListener() {},
    querySelectorAll(selector) { return selector === 'a[href^="#"]' ? links : []; },
  };
  const sections = [{ id: 'today' }, { id: '' }, { id: 'status' }, { id: 'doctor' }];
  let callback;
  let options;
  const observed = [];
  class FakeObserver {
    constructor(cb, opts) { callback = cb; options = opts; }
    observe(target) { observed.push(target); }
  }
  const nodes = { '.site-header nav': nav };
  const document = {
    querySelector(selector) { return nodes[selector] || null; },
    querySelectorAll(selector) { return selector === 'main section' ? sections : []; },
    documentElement: { classList: { add() {} } },
  };
  vm.runInNewContext(script, { document, IntersectionObserver: FakeObserver }, { timeout: 1000, filename: 'site.js' });
  assert.equal(observed.length, 4);
  assert.equal(options.rootMargin, '-50% 0px -50% 0px');
  const current = () => links.map((link) => link.getAttribute('aria-current') || '');
  assert.deepEqual(current(), ['', '', '']);
  callback([{ isIntersecting: true, target: sections[2] }]);
  assert.deepEqual(current(), ['', '', 'location']);
  assert.equal(nav.scrollLeft, 240);
  callback([{ isIntersecting: false, target: sections[0] }]);
  assert.deepEqual(current(), ['', '', 'location']);
  callback([{ isIntersecting: true, target: sections[3] }]);
  assert.deepEqual(current(), ['', '', '']);
  assert.equal(nav.scrollLeft, 240);
  callback([{ isIntersecting: true, target: sections[0] }]);
  assert.deepEqual(current(), ['location', '', '']);
  assert.equal(nav.scrollLeft, 0);
});

test('returning to the first section scrolls the phone nav row back to its start', () => {
  const link = { offsetLeft: 300, offsetWidth: 80, getAttribute() { return '#status'; }, setAttribute() {}, removeAttribute() {} };
  const nav = { scrollLeft: 0, scrollWidth: 500, clientWidth: 200, addEventListener() {}, querySelectorAll() { return [link]; } };
  const sections = [{ id: '' }, { id: 'status' }];
  let callback;
  class FakeObserver { constructor(cb) { callback = cb; } observe() {} }
  const document = {
    querySelector(selector) { return selector === '.site-header nav' ? nav : null; },
    querySelectorAll(selector) { return selector === 'main section' ? sections : []; },
    documentElement: { classList: { add() {} } },
  };
  vm.runInNewContext(script, { document, IntersectionObserver: FakeObserver }, { timeout: 1000, filename: 'site.js' });
  callback([{ isIntersecting: true, target: sections[1] }]);
  assert.equal(nav.scrollLeft, 240);
  callback([{ isIntersecting: true, target: sections[0] }]);
  assert.equal(nav.scrollLeft, 0);
});

test('without IntersectionObserver the nav is left unmarked', () => {
  const { nodes } = workbench();
  assert.equal(nodes['#demo-controls'].disabled, false);
});
