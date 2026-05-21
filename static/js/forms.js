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
    el.style.display = 'block';
    el.textContent = msg;
    field.insertAdjacentElement('afterend', el);
  }

  // ── Toggle dependent field visibility ────────────────────────────────────
  // Usage: <input data-toggle-field="#targetId" data-toggle-value="1">
  function initDependentFields() {
    document.querySelectorAll('[data-toggle-field]').forEach(function (trigger) {
      function update() {
        var target    = document.querySelector(trigger.dataset.toggleField);
        var showValue = trigger.dataset.toggleValue;
        if (!target) return;
        var isChecked = (trigger.type === 'checkbox') ? trigger.checked : trigger.value === showValue;
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

  // ── Check if a field has no meaningful value ──────────────────────────────
  // Works for <input>, <select>, <textarea>
  function fieldIsEmpty(field) {
    var val = field.value;
    // Empty string, whitespace-only, or the default blank select option
    return !val || val.trim() === '' || val === '0' || val === '---------';
  }

  // ── Required field validation with styled messages ────────────────────────
  // Replaces the invisible browser bubble with a visible .invalid-feedback div
  function initRequiredValidation() {
    document.querySelectorAll('form').forEach(function (form) {

      // Suppress all native browser validation UI
      form.setAttribute('novalidate', '');

      form.addEventListener('submit', function (e) {
        var hasErrors = false;

        form.querySelectorAll('[required]').forEach(function (field) {
          // Clear previous error for this field
          clearFieldError(field);

          if (fieldIsEmpty(field)) {
            e.preventDefault();
            e.stopImmediatePropagation(); // stop initSubmitGuard from disabling button
            hasErrors = true;
            showFieldError(field, 'This field is required.');
          }
        });

        if (hasErrors) {
          // Scroll to first invalid field
          var first = form.querySelector('.is-invalid');
          if (first) first.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      // Use capture=true so this runs BEFORE initSubmitGuard's submit handler
      }, true);

      // Clear error as soon as user starts filling the field
      form.querySelectorAll('[required]').forEach(function (field) {
        field.addEventListener('input', function () { clearFieldError(field); });
        field.addEventListener('change', function () { clearFieldError(field); });
      });
    });
  }

  function clearFieldError(field) {
    field.classList.remove('is-invalid');
    // Remove only the .invalid-feedback we injected (not server-side ones)
    var fb = field.parentNode.querySelector('.invalid-feedback[data-js]');
    if (fb) fb.remove();
  }

  function showFieldError(field, msg) {
    field.classList.add('is-invalid');
    var existing = field.parentNode.querySelector('.invalid-feedback[data-js]');
    if (existing) { existing.textContent = msg; return; }
    var el = document.createElement('div');
    el.className = 'invalid-feedback';
    el.setAttribute('data-js', ''); // mark as JS-injected so we can remove it cleanly
    el.style.display = 'block';
    el.textContent = msg;
    field.insertAdjacentElement('afterend', el);
  }

  // ── Disable submit on double-click ───────────────────────────────────────
  // Runs AFTER validation (capture=false, which is default)
  function initSubmitGuard() {
    document.querySelectorAll('form[data-submit-once]').forEach(function (form) {
        form.addEventListener('submit', function (e) {
            // Do not disable if validation errors are present
            if (form.querySelector('.is-invalid')) return;
            // Do not disable if event was prevented by validation
            if (e.defaultPrevented) return;
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
    initRequiredValidation(); // must come before initSubmitGuard
    initSubmitGuard();
  });

})();
