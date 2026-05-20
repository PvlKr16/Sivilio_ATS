/**
 * forms.js — Form-related JS utilities
 * Client-side validation hints, avatar/logo preview, dynamic nested forms
 * HR IT Platform
 */

(function () {
  'use strict';

  // ── Image preview for file inputs (avatar / logo) ─────────────────────────
  function initImagePreview() {
    document.querySelectorAll('[data-preview-target]').forEach(function (input) {
      var targetId = input.dataset.previewTarget;
      var preview  = document.getElementById(targetId);
      if (!preview) return;

      input.addEventListener('change', function () {
        var file = this.files[0];
        if (!file) return;

        if (!file.type.startsWith('image/')) {
          showFieldError(input, 'Please select an image file.');
          return;
        }
        if (file.size > 5 * 1024 * 1024) {
          showFieldError(input, 'Image must be smaller than 5 MB.');
          return;
        }

        var reader = new FileReader();
        reader.onload = function (e) {
          if (preview.tagName === 'IMG') {
            preview.src = e.target.result;
            preview.style.display = '';
          } else {
            // Avatar placeholder div — swap its content
            preview.innerHTML = '<img src="' + e.target.result + '" alt="Preview" style="width:100%;height:100%;object-fit:cover;border-radius:inherit">';
          }
        };
        reader.readAsDataURL(file);
      });
    });
  }

  // ── Show inline error on a field ─────────────────────────────────────────
  function showFieldError(field, msg) {
    field.classList.add('is-invalid');
    var existing = field.parentNode.querySelector('.invalid-feedback');
    if (existing) { existing.textContent = msg; return; }
    var el = document.createElement('div');
    el.className = 'invalid-feedback';
    el.textContent = msg;
    field.insertAdjacentElement('afterend', el);
  }

  // ── Toggle dependent field visibility ────────────────────────────────────
  // Usage: <input data-toggle-field="#targetId" data-toggle-value="1">
  function initDependentFields() {
    document.querySelectorAll('[data-toggle-field]').forEach(function (trigger) {
      function update() {
        var target     = document.querySelector(trigger.dataset.toggleField);
        var showValue  = trigger.dataset.toggleValue;
        if (!target) return;
        var isChecked  = (trigger.type === 'checkbox') ? trigger.checked : trigger.value === showValue;
        target.style.display = isChecked ? '' : 'none';
      }
      trigger.addEventListener('change', update);
      update(); // run once on init
    });
  }

  // ── Work experience: is_current hides date_end ────────────────────────────
  function initWorkCurrentToggle() {
    document.querySelectorAll('[data-work-current]').forEach(function (checkbox) {
      var dateEndGroup = document.getElementById('date-end-group');
      if (!dateEndGroup) return;

      function toggle() {
        dateEndGroup.style.display = checkbox.checked ? 'none' : '';
      }
      checkbox.addEventListener('change', toggle);
      toggle();
    });
  }

  // ── Character counter for textarea ───────────────────────────────────────
  function initCharCounters() {
    document.querySelectorAll('[data-max-chars]').forEach(function (el) {
      var max     = parseInt(el.dataset.maxChars, 10);
      var counter = document.createElement('div');
      counter.className = 'form-text text-muted char-counter';
      el.insertAdjacentElement('afterend', counter);

      function update() {
        var remaining = max - el.value.length;
        counter.textContent = remaining + ' characters remaining';
        counter.style.color = remaining < 20 ? 'var(--color-danger)' : '';
      }
      el.addEventListener('input', update);
      update();
    });
  }

  // ── Disable submit on double-click ───────────────────────────────────────
  function initSubmitGuard() {
    document.querySelectorAll('form[data-submit-once]').forEach(function (form) {
      form.addEventListener('submit', function () {
        var btn = form.querySelector('[type="submit"]');
        if (!btn) return;
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving…';
      });
    });
  }

  // ── Init ─────────────────────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', function () {
    initImagePreview();
    initDependentFields();
    initWorkCurrentToggle();
    initCharCounters();
    initSubmitGuard();
  });

})();
