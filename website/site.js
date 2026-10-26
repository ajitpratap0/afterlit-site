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
  const tones = { warm: 'Warm white', amber: 'Amber', sage: 'Sage', blue: 'Blue' };
  let tone = 'warm';
  function update() {
    const level = Number(brightness.value);
    lamp.className = 'demo-lamp level-' + level + ' tone-' + tone;
    brightness.setAttribute('aria-valuetext', level === 0 ? 'Off' : level + '%');
    value.value = level + '%';
    value.textContent = level + '%';
    power.textContent = level === 0 ? 'Off' : 'On';
    levelText.textContent = level + '%';
    colorText.textContent = tones[tone];
    for (const swatch of swatches) swatch.setAttribute('aria-pressed', String(swatch.dataset.tone === tone));
  }
  brightness.addEventListener('input', update);
  for (const swatch of swatches) {
    swatch.addEventListener('click', () => {
      const selected = swatch.dataset.tone;
      if (!selected || !(selected in tones)) return;
      tone = selected;
      update();
    });
  }
  controls.disabled = false;
  document.documentElement.classList.add('js-ready');
  update();
})();
