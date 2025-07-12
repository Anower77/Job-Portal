// Sidebar toggle for mobile
const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
if (sidebar && sidebarToggle) {
  sidebarToggle.addEventListener('click', function() {
    sidebar.classList.toggle('open');
  });
}

// Filter button active state
const filterBtns = document.querySelectorAll('.filter-btn');
filterBtns.forEach(btn => {
  btn.addEventListener('click', function() {
    filterBtns.forEach(b => b.classList.remove('active'));
    this.classList.add('active');
    // Optionally, filter job cards here
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