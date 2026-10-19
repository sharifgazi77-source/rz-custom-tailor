(() => {
  const body = document.body;
  const menu = document.querySelector('.menu-toggle');
  menu?.addEventListener('click', () => document.querySelector('.site-header').classList.toggle('menu-open'));
  document.querySelectorAll('.site-header nav a').forEach(a => a.addEventListener('click', () => document.querySelector('.site-header').classList.remove('menu-open')));

  let selected = { name: 'Midnight wool', color: '#26343b' };
  const previewCoat = document.querySelector('.preview-coat');
  const updateDesign = () => {
    if (!previewCoat) return;
    previewCoat.style.background = `linear-gradient(100deg,color-mix(in srgb,${selected.color},#111 22%),${selected.color} 50%,color-mix(in srgb,${selected.color},#111 22%))`;
    document.querySelector('#previewSummary').textContent = `${selected.name} · ${document.querySelector('#lapel').value} · ${document.querySelector('#buttons').value}`;
  };
  document.querySelectorAll('.swatch-option').forEach(btn => btn.addEventListener('click', () => {
    document.querySelectorAll('.swatch-option').forEach(b => b.classList.remove('selected'));
    btn.classList.add('selected'); selected = { name: btn.dataset.name, color: btn.dataset.color }; updateDesign();
  }));
  ['lapel', 'buttons', 'pocket', 'fit'].forEach(id => document.querySelector(`#${id}`)?.addEventListener('change', updateDesign));

  const modal = document.querySelector('#orderModal');
  const makeOrder = () => {
    const design = `${selected.name}; ${document.querySelector('#lapel').value}; ${document.querySelector('#buttons').value}; ${document.querySelector('#pocket').value}; ${document.querySelector('#fit').value}; Measurements (${document.querySelector('#unit').value}) — chest ${document.querySelector('#chest').value || 'not supplied'}, waist ${document.querySelector('#waist').value || 'not supplied'}, sleeve ${document.querySelector('#sleeve').value || 'not supplied'}`;
    document.querySelector('#formItem').value = document.querySelector('#previewName').textContent;
    document.querySelector('#formDetails').value = design;
    modal?.classList.add('open'); document.querySelector('#orderModal input')?.focus();
  };
  document.querySelector('#saveDesign')?.addEventListener('click', makeOrder);
  document.querySelector('#closeModal')?.addEventListener('click', () => modal.classList.remove('open'));
  modal?.addEventListener('click', e => { if (e.target === modal) modal.classList.remove('open'); });
  document.querySelector('#shareDesign')?.addEventListener('click', async e => {
    const summary = `${selected.name}; ${document.querySelector('#previewSummary').textContent}`;
    try { await navigator.clipboard.writeText(summary); e.currentTarget.textContent = '✓'; setTimeout(() => e.currentTarget.textContent = '↗', 1200); }
    catch { window.prompt('Copy your design:', summary); }
  });

  const slides = [...document.querySelectorAll('.spotlight-slide')];
  let activeSlide = 0;
  const paintSlide = (index) => {
    if (!slides.length) return;
    activeSlide = (index + slides.length) % slides.length;
    slides.forEach((slide, i) => slide.classList.toggle('is-active', i === activeSlide));
    const counter = document.querySelector('#spotCount');
    if (counter) counter.textContent = `${String(activeSlide + 1).padStart(2,'0')} / ${String(slides.length).padStart(2,'0')}`;
  };
  document.querySelector('#spotPrev')?.addEventListener('click', () => { paintSlide(activeSlide - 1); resetAuto(); });
  document.querySelector('#spotNext')?.addEventListener('click', () => { paintSlide(activeSlide + 1); resetAuto(); });
  let autoTimer = slides.length > 1 ? setInterval(() => paintSlide(activeSlide + 1), 4800) : null;
  function resetAuto(){ if (autoTimer) clearInterval(autoTimer); autoTimer = slides.length > 1 ? setInterval(() => paintSlide(activeSlide + 1), 4800) : null; }
  paintSlide(0);

  const datePicker = document.querySelector('input[name="preferred_date"]');
  if (datePicker) datePicker.min = new Date().toISOString().slice(0, 10);
})();
