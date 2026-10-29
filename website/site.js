(() => {
  const controls = document.querySelector('#demo-controls');
  const brightness = document.querySelector('#brightness');
  const lamp = document.querySelector('#demo-lamp');
  const value = document.querySelector('#brightness-value');
  const reqPower = document.querySelector('#req-power');
  const reqLevel = document.querySelector('#req-level');
  const reqColor = document.querySelector('#req-color');
  const power = document.querySelector('#state-power');
  const levelText = document.querySelector('#state-level');
  const colorText = document.querySelector('#state-color');
  const swatches = [...document.querySelectorAll('.swatch')];
  if (!controls || !brightness || !lamp || !value || !reqPower || !reqLevel || !reqColor
    || !power || !levelText || !colorText || !swatches.length) return;
  const readback = document.querySelector('.readback');
  const offNote = document.querySelector('#color-off-note');
  const swatchGroup = document.querySelector('.swatches');
  // With JS the note keeps its space (visibility, not display) so the readback never jumps.
  if (offNote) offNote.hidden = false;
  // Readback values that get a pencil stroke when a user change rewrites them.
  // Requested and reported strokes draw together: a stagger would fake a device round trip.
  const rows = [reqPower, reqLevel, reqColor, power, levelText, colorText];
  const tones = { warm: 'Warm white', amber: 'Amber', sage: 'Sage', blue: 'Blue' };
  let tone = 'warm';
  let changed = [];
  // Only rewrite text that changed, so the polite live region is not re-announced on load.
  const set = (el, text) => { if (el.textContent !== text) { el.textContent = text; changed.push(el); } };
  const isOff = () => Number(brightness.value) === 0;
  function update() {
    changed = [];
    const level = Number(brightness.value);
    const off = level === 0;
    lamp.className = 'demo-lamp level-' + level + ' tone-' + tone;
    brightness.setAttribute('aria-valuetext', off ? 'Off' : level + '%');
    value.value = level + '%';
    set(value, level + '%');
    // A lamp that is off has no colour, so neither step may name one.
    const requested = { power: off ? 'Off' : 'On', level: level + '%', color: off ? 'None' : tones[tone] };
    // Step 1: what this page asked the simulated lamp for.
    set(reqPower, requested.power);
    set(reqLevel, requested.level);
    set(reqColor, requested.color);
    // Step 2: what the simulated lamp reports back. In this browser simulation it always
    // echoes the request, in the same frame; no delay or device approval is faked.
    const reported = { ...requested };
    set(power, reported.power);
    set(levelText, reported.level);
    set(colorText, reported.color);
    for (const swatch of swatches) {
      swatch.setAttribute('aria-pressed', String(swatch.dataset.tone === tone));
      swatch.disabled = off;
    }
    if (offNote) offNote.classList.toggle('is-shown', off);
    // Describe the group by the note only while it is true, or screen readers announce it anyway.
    if (swatchGroup) {
      if (off) swatchGroup.setAttribute('aria-describedby', 'color-off-note');
      else swatchGroup.removeAttribute('aria-describedby');
    }
  }
  // The readback text already updated synchronously in update(). This only replays the
  // confirmation dot and redraws the pencil stroke under each value that changed.
  // A change that rewrites no readback value leaves the existing strokes in place.
  function confirmReadback() {
    if (!readback || !readback.classList) return;
    const fresh = rows.filter((row) => row.classList && changed.includes(row));
    readback.classList.remove('is-confirmed');
    if (fresh.length) for (const row of rows) if (row.classList) row.classList.remove('is-fresh');
    void readback.offsetWidth;
    readback.classList.add('is-confirmed');
    for (const row of fresh) row.classList.add('is-fresh');
  }
  brightness.addEventListener('input', () => { update(); confirmReadback(); });
  for (const swatch of swatches) {
    swatch.addEventListener('click', () => {
      const selected = swatch.dataset.tone;
      if (isOff() || !selected || !Object.prototype.hasOwnProperty.call(tones, selected)) return;
      tone = selected;
      update();
      confirmReadback();
    });
  }
  // Reset returns to the starting state through the same update(), so the readback
  // reports it like any other change. Browser only: nothing is sent anywhere.
  const reset = document.querySelector('#demo-reset');
  if (reset && typeof reset.addEventListener === 'function') {
    reset.addEventListener('click', () => {
      brightness.value = '75';
      tone = 'warm';
      update();
      confirmReadback();
    });
  }
  controls.disabled = false;
  document.documentElement.classList.add('js-ready');
  update();
})();

// If the nav row ever overflows sideways, bring a keyboard-focused
// link fully into view so its focus ring is not cut off at the row's edge.
(() => {
  const nav = document.querySelector('.site-header nav');
  if (!nav || typeof nav.addEventListener !== 'function') return;
  nav.addEventListener('focusin', (event) => {
    const link = event && event.target;
    if (link && typeof link.scrollIntoView === 'function') {
      link.scrollIntoView({ block: 'nearest', inline: 'nearest' });
    }
  });
})();

// Show where the reader is: the nav link for the section crossing the middle of the
// screen gets aria-current="location". On phones the sideways nav row also scrolls so
// that link is in view. Sections without a nav link clear the mark.
(() => {
  const nav = document.querySelector('.site-header nav');
  const Observer = typeof IntersectionObserver === 'function' ? IntersectionObserver : null;
  if (!nav || !Observer || typeof nav.querySelectorAll !== 'function') return;
  const links = new Map();
  for (const link of nav.querySelectorAll('a[href^="#"]')) {
    links.set(link.getAttribute('href').slice(1), link);
  }
  const sections = [...document.querySelectorAll('main section')];
  if (!links.size || !sections.length) return;
  const mark = (id, atTop) => {
    const current = links.get(id) || null;
    for (const link of links.values()) {
      if (link === current) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    }
    // Only scroll the row sideways, never the page, and without animation.
    if (current && nav.scrollWidth > nav.clientWidth) {
      const left = current.offsetLeft - (nav.clientWidth - current.offsetWidth) / 2;
      nav.scrollLeft = Math.max(0, left);
    } else if (atTop) {
      nav.scrollLeft = 0;
    }
  };
  const observer = new Observer((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting && entry.target) mark(entry.target.id || '', entry.target === sections[0]);
    }
  }, { rootMargin: '-50% 0px -50% 0px' });
  for (const section of sections) observer.observe(section);
})();
