/**
 * ui.js — General UI utilities
 * Alert dismissal, tab switching, delete confirmations, tooltips
 * HR IT Platform
 */

(function () {
  'use strict';

  // ── Auto-dismiss flash messages ───────────────────────────────────────────
  function initAlerts() {
    document.querySelectorAll('.alert[data-auto-dismiss]').forEach(function (el) {
      var delay = parseInt(el.dataset.autoDismiss, 10) || 4000;
      setTimeout(function () { dismissAlert(el); }, delay);
    });

    // Manual close buttons
    document.querySelectorAll('.alert-close').forEach(function (btn) {
      btn.addEventListener('click', function () {
        dismissAlert(btn.closest('.alert'));
      });
    });
  }

  function dismissAlert(el) {
    if (!el) return;
    el.style.transition = 'opacity 0.3s ease, max-height 0.4s ease, margin 0.4s ease, padding 0.4s ease';
    el.style.opacity = '0';
    el.style.maxHeight = el.offsetHeight + 'px';
    requestAnimationFrame(function () {
      el.style.maxHeight = '0';
      el.style.marginBottom = '0';
      el.style.paddingTop = '0';
      el.style.paddingBottom = '0';
    });
    setTimeout(function () { el.remove(); }, 450);
  }

  // ── Tab switching ─────────────────────────────────────────────────────────
  function initTabs() {
    document.querySelectorAll('[data-tab-target]').forEach(function (trigger) {
      trigger.addEventListener('click', function (e) {
        e.preventDefault();
        var targetId = this.dataset.tabTarget;
        var container = this.closest('[data-tabs]') || document;

        // Deactivate all tabs & panes in the same group
        var group = this.closest('.tab-nav');
        if (group) {
          group.querySelectorAll('.tab-link').forEach(function (t) { t.classList.remove('active'); });
        }
        container.querySelectorAll('.tab-pane').forEach(function (p) { p.classList.remove('active'); });

        // Activate selected
        this.classList.add('active');
        var pane = document.getElementById(targetId);
        if (pane) pane.classList.add('active');

        // Persist selection in URL hash without scrolling
        history.replaceState(null, '', '#' + targetId);
      });
    });

    // Restore active tab from URL hash on page load
    var hash = window.location.hash.replace('#', '');
    if (hash) {
      var trigger = document.querySelector('[data-tab-target="' + hash + '"]');
      if (trigger) trigger.click();
    } else {
      // Activate the first tab in each nav if none is active
      document.querySelectorAll('.tab-nav').forEach(function (nav) {
        if (!nav.querySelector('.tab-link.active')) {
          var first = nav.querySelector('.tab-link');
          if (first) first.click();
        }
      });
    }
  }

  // ── Delete confirmations ──────────────────────────────────────────────────
  function initDeleteConfirm() {
    document.querySelectorAll('[data-confirm]').forEach(function (el) {
      el.addEventListener('click', function (e) {
        var msg = this.dataset.confirm || 'Are you sure you want to delete this record?';
        if (!window.confirm(msg)) {
          e.preventDefault();
          e.stopPropagation();
        }
      });
    });
  }

  // ── Simple tooltip (title-based) ─────────────────────────────────────────
  function initTooltips() {
    // Uses native title attribute — browsers handle this;
    // for fancier tooltips replace with a lightweight library.
    document.querySelectorAll('[data-tooltip]').forEach(function (el) {
      if (!el.title) el.title = el.dataset.tooltip;
    });
  }

  // ── Initialise everything on DOM ready ───────────────────────────────────
  document.addEventListener('DOMContentLoaded', function () {
    initAlerts();
    initTabs();
    initDeleteConfirm();
    initTooltips();
  });

})();
