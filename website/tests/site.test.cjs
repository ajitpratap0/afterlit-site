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
    ...extra,
    addEventListener(name, callback) { listeners.set(name, callback); },
    setAttribute(name, value) { attributes.set(name, value); },
    getAttribute(name) { return attributes.get(name); },
    fire(name) { assert.ok(listeners.has(name), `missing ${name} listener`); listeners.get(name)(); },
  };
}

function workbench(missing) {
  const nodes = {
    '#demo-controls': element({ disabled: true }),
    '#brightness': element({ value: '75' }),
    '#demo-lamp': element({ className: 'demo-lamp level-75 tone-warm' }),
    '#brightness-value': element({ value: '75%' }),
    '#state-power': element({ textContent: 'On' }),
    '#state-level': element({ textContent: '75%' }),
    '#state-color': element({ textContent: 'Warm white' }),
  };
  const swatches = ['warm', 'amber', 'sage', 'blue'].map((tone) => element({ dataset: { tone } }));
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
