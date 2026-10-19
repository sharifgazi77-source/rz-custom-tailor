(() => {
  const colorInput = document.querySelector('#colorInput');
  const colorLabel = document.querySelector('#selectedColor');
  document.querySelectorAll('.color-chip').forEach(button => button.addEventListener('click', () => {
    document.querySelectorAll('.color-chip').forEach(b => b.classList.remove('selected'));
    button.classList.add('selected'); colorInput.value = button.dataset.color; colorLabel.textContent = button.dataset.color;
  }));
  const sizeInput = document.querySelector('#sizeInput');
  document.querySelectorAll('.size-chip').forEach(button => button.addEventListener('click', () => {
    document.querySelectorAll('.size-chip').forEach(b => b.classList.remove('selected'));
    button.classList.add('selected'); sizeInput.value = button.dataset.size;
  }));
  const quantity = document.querySelector('#quantity');
  document.querySelector('#qtyDown')?.addEventListener('click', () => quantity.value = Math.max(1, Number(quantity.value || 1) - 1));
  document.querySelector('#qtyUp')?.addEventListener('click', () => quantity.value = Math.min(20, Number(quantity.value || 1) + 1));
  const guide = document.querySelector('#sizeModal');
  document.querySelector('#sizeGuide')?.addEventListener('click', () => guide.classList.add('open'));
  document.querySelector('#closeSize')?.addEventListener('click', () => guide.classList.remove('open'));
  guide?.addEventListener('click', e => { if (e.target === guide) guide.classList.remove('open'); });
})();
