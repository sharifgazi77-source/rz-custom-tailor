(() => {
  const modal = document.querySelector('#productModal');
  const show = () => modal.classList.add('open');
  const clear = () => {
    document.querySelector('#productFormTitle').textContent = 'Add product';
    ['productId','productName','productDescription','productPrice','productColors','productSizes'].forEach(id => document.querySelector(`#${id}`).value = '');
    document.querySelector('#productCategory').selectedIndex = 0;
    document.querySelector('#productColor').value = '#26343b';
    document.querySelector('#productFeatured').checked = false;
  };
  document.querySelector('#addProduct')?.addEventListener('click', () => { clear(); show(); });
  document.querySelector('#closeProduct')?.addEventListener('click', () => modal.classList.remove('open'));
  modal?.addEventListener('click', e => { if (e.target === modal) modal.classList.remove('open'); });
  document.querySelectorAll('.edit-btn[data-id]').forEach(btn => btn.addEventListener('click', () => {
    document.querySelector('#productFormTitle').textContent = 'Edit product';
    document.querySelector('#productId').value = btn.dataset.id;
    document.querySelector('#productName').value = btn.dataset.name;
    document.querySelector('#productCategory').value = btn.dataset.categoryId;
    document.querySelector('#productDescription').value = btn.dataset.description;
    document.querySelector('#productPrice').value = btn.dataset.price;
    document.querySelector('#productColor').value = btn.dataset.color;
    document.querySelector('#productColors').value = btn.dataset.colors || '';
    document.querySelector('#productSizes').value = btn.dataset.sizes || '';
    document.querySelector('#productFeatured').checked = btn.dataset.featured === '1';
    show();
  }));
})();
