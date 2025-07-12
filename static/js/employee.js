// Sidebar toggle for mobile
const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
if (sidebar && sidebarToggle) {
  sidebarToggle.addEventListener('click', function() {
    sidebar.classList.toggle('open');
  });
}

// Tab/filter switching
const filterBtns = document.querySelectorAll('.filter-btn');
const tabSections = document.querySelectorAll('.tab-section');
filterBtns.forEach(btn => {
  btn.addEventListener('click', function() {
    filterBtns.forEach(b => b.classList.remove('active'));
    this.classList.add('active');
    const section = this.getAttribute('data-section');
    tabSections.forEach(tab => {
      if (tab.id === section) {
        tab.style.display = '';
        tab.classList.add('show');
      } else {
        tab.style.display = 'none';
        tab.classList.remove('show');
      }
    });
  });
});

// Close sidebar when clicking outside (mobile)
document.addEventListener('click', function(e) {
  if (window.innerWidth <= 900 && sidebar && sidebar.classList.contains('open')) {
    if (!sidebar.contains(e.target) && e.target !== sidebarToggle) {
      sidebar.classList.remove('open');
    }
  }
}); 