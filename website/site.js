(() => {
  const controls = document.querySelector('#demo-controls');
  const brightness = document.querySelector('#brightness');
  const lamp = document.querySelector('#demo-lamp');
  const value = document.querySelector('#brightness-value');
  const power = document.querySelector('#state-power');
  const levelText = document.querySelector('#state-level');
  const colorText = document.querySelector('#state-color');
  const swatches = [...document.querySelectorAll('.swatch')];
  if (!controls || !brightness || !lamp || !value || !power || !levelText || !colorText || !swatches.length) return;
  const readback = document.querySelector('.readback');
  const tones = { warm: 'Warm white', amber: 'Amber', sage: 'Sage', blue: 'Blue' };
  let tone = 'warm';
  // Only rewrite text that changed, so the polite live region is not re-announced on load.
  const set = (el, text) => { if (el.textContent !== text) el.textContent = text; };
  function update() {
    const level = Number(brightness.value);
    lamp.className = 'demo-lamp level-' + level + ' tone-' + tone;
    brightness.setAttribute('aria-valuetext', level === 0 ? 'Off' : level + '%');
    value.value = level + '%';
    set(value, level + '%');
    set(power, level === 0 ? 'Off' : 'On');
    set(levelText, level + '%');
    set(colorText, tones[tone]);
    for (const swatch of swatches) swatch.setAttribute('aria-pressed', String(swatch.dataset.tone === tone));
  }
  // The readback text updates synchronously; this only replays the confirmation dot.
  function confirmReadback() {
    if (!readback || !readback.classList) return;
    readback.classList.remove('is-confirmed');
    void readback.offsetWidth;
    readback.classList.add('is-confirmed');
  }
  brightness.addEventListener('input', () => { update(); confirmReadback(); });
  for (const swatch of swatches) {
    swatch.addEventListener('click', () => {
      const selected = swatch.dataset.tone;
      if (!selected || !Object.prototype.hasOwnProperty.call(tones, selected)) return;
      tone = selected;
      update();
      confirmReadback();
    });
  }
  controls.disabled = false;
  document.documentElement.classList.add('js-ready');
  update();
})();
