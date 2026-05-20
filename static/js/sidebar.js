/**
 * sidebar.js — Sidebar toggle, mobile drawer, active link highlighting
 * HR IT Platform
 */

(function () {
  'use strict';

  // ── Elements ──────────────────────────────────────────────────────────────
  const sidebar        = document.getElementById('sidebar');
  const sidebarToggle  = document.getElementById('sidebarToggle');
  const sidebarOverlay = document.getElementById('sidebarOverlay');

  if (!sidebar) return;

  // ── Mobile drawer toggle ──────────────────────────────────────────────────
  function openSidebar() {
    sidebar.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeSidebar() {
    sidebar.classList.remove('open');
    document.body.style.overflow = '';
  }

  if (sidebarToggle) {
    sidebarToggle.addEventListener('click', function () {
      sidebar.classList.contains('open') ? closeSidebar() : openSidebar();
    });
  }

  if (sidebarOverlay) {
    sidebarOverlay.addEventListener('click', closeSidebar);
  }

  // Close sidebar when navigating on mobile
  sidebar.querySelectorAll('.sidebar-link').forEach(function (link) {
    link.addEventListener('click', function () {
      if (window.innerWidth <= 768) closeSidebar();
    });
  });

  // ── Active link highlighting ──────────────────────────────────────────────
  // Mark the link whose href best matches the current path
  var currentPath = window.location.pathname;

  sidebar.querySelectorAll('.sidebar-link[href]').forEach(function (link) {
    var href = link.getAttribute('href');
    if (!href || href === '#') return;

    // Exact match takes priority; otherwise prefix match (e.g. /people/ matches /people/42/)
    var isExact  = currentPath === href;
    var isPrefix = href !== '/' && currentPath.startsWith(href);

    if (isExact || isPrefix) {
      link.classList.add('active');
    }
  });

  // ── Keyboard navigation ───────────────────────────────────────────────────
  document.addEventListener('keydown', function (e) {
    // Press Escape to close mobile sidebar
    if (e.key === 'Escape' && sidebar.classList.contains('open')) {
      closeSidebar();
    }
  });

})();
