document.addEventListener('DOMContentLoaded', function () {
  const selectAll = document.getElementById('select-all');
  if (selectAll) {
    selectAll.addEventListener('change', function () {
      const checkboxes = document.querySelectorAll('.activity-checkbox');
      checkboxes.forEach(cb => cb.checked = this.checked);
    });
  }
});
