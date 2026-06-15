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
      // Skip the language switcher form — it must never be intercepted.
      if (form.querySelector('[name="language"]')) return;

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

// ── CV drag & drop zone ───────────────────────────────────────────────────
// Initialises a single [data-drop-zone] element.
// The zone must contain a .cv-drop-input-wrap > input[type="file"] subtree.
// After init the real <input> is moved to be a direct child of the zone so it
// covers the whole clickable/droppable area via position:absolute styling.
function initDropZone(zone) {
  // Input may be nested inside an extra .ef-file span that Django renders,
  // so search anywhere inside the zone rather than only in .cv-drop-input-wrap
  var input = zone.querySelector('input[type="file"]');
  if (!input) return;

  // Relocate the real input directly into zone so it covers the whole area
  input.classList.add('cv-drop-input');
  zone.appendChild(input);

  var textEl     = zone.querySelector('.cv-drop-text');
  var hintEl     = zone.querySelector('.cv-drop-hint');
  var iconEl     = zone.querySelector('.cv-drop-icon');
  var filenameEl = zone.querySelector('.cv-drop-filename');

  function setFile(name) {
    if (name) {
      zone.classList.add('has-file');
      if (filenameEl) { filenameEl.textContent = name; filenameEl.style.display = ''; }
      if (textEl) textEl.style.display = 'none';
      if (hintEl) hintEl.style.display = 'none';
      if (iconEl) iconEl.className = 'fas fa-check cv-drop-icon';
    } else {
      zone.classList.remove('has-file');
      if (filenameEl) filenameEl.style.display = 'none';
      if (textEl) textEl.style.display = '';
      if (hintEl) hintEl.style.display = '';
      if (iconEl) iconEl.className = 'fas fa-file-arrow-up cv-drop-icon';
    }
  }

  input.addEventListener('change', function () {
    setFile(this.files[0] ? this.files[0].name : '');
  });

  zone.addEventListener('dragover', function (e) {
    e.preventDefault();
    zone.classList.add('dragover');
  });
  zone.addEventListener('dragleave', function () {
    zone.classList.remove('dragover');
  });
  zone.addEventListener('drop', function (e) {
    e.preventDefault();
    zone.classList.remove('dragover');
    if (e.dataTransfer.files.length) {
      try {
        var dt = new DataTransfer();
        dt.items.add(e.dataTransfer.files[0]);
        input.files = dt.files;
        setFile(e.dataTransfer.files[0].name);
      } catch (_) { /* Safari fallback: DataTransfer assignment not supported */ }
    }
  });
}

// Initialise all drop zones already present in the DOM on page load.
// Newly added formset rows must call initDropZone() themselves after insertion.
function initCvDropZone() {
  document.querySelectorAll('[data-drop-zone]').forEach(initDropZone);
}

// Expose initDropZone so people_form.js can call it for dynamically added rows
window.HRForms = window.HRForms || {};
window.HRForms.initDropZone = initDropZone;

  // ── Form state persistence across language switches ───────────────────────
  //
  // Django's set_language view redirects back to the same URL, wiping unsaved
  // form data.  We intercept the language <select> change, snapshot every
  // serialisable field into sessionStorage, then restore on the next load.
  //
  // The language switcher uses onchange="this.form.submit()" in the HTML, so
  // we intercept at the form's submit event (which fires after onchange) and
  // also listen directly on the select's change event — whichever fires first.
  //
  // Restore runs after a short delay so Select2 (loaded in extra_js block,
  // after this file) has time to initialise before we trigger its .val().

  var FORM_STATE_KEY_PREFIX = 'hr_form_state:';

  function _formStateKey() {
    // Strip the language prefix (e.g. /be/, /de/, /ru/) so the key stays the
    // same regardless of which language the user switches to.
    var path = window.location.pathname.replace(/^\/[a-z]{2}\//, '/');
    return FORM_STATE_KEY_PREFIX + path;
  }

  // Is this the language-switcher form?
  function _isLangForm(form) {
    return !!form.querySelector('[name="language"]');
  }

  // Collect serialisable values from all non-language forms on the page.
  function _collectFormState() {
    var state = { _fields: {}, _selects: {} };

    document.querySelectorAll('form').forEach(function (form) {
      if (_isLangForm(form)) return;

      form.querySelectorAll('input, textarea').forEach(function (el) {
        if (!el.name || el.name === 'csrfmiddlewaretoken') return;
        if (el.type === 'file') return;
        if (el.type === 'checkbox' || el.type === 'radio') {
          state._fields[el.name + '::' + el.value] = el.checked;
        } else {
          state._fields[el.name] = el.value;
        }
      });

      form.querySelectorAll('select').forEach(function (el) {
        if (!el.name) return;
        var vals = [];
        Array.prototype.forEach.call(el.options, function (opt) {
          if (opt.selected) vals.push(opt.value);
        });
        state._selects[el.name] = vals;
      });
    });

    return state;
  }

  // Write state to sessionStorage before language redirect.
  function _saveFormState() {
    var state = _collectFormState();
    var hasData = Object.keys(state._fields).length > 0 ||
                  Object.keys(state._selects).length > 0;
    if (!hasData) return;
    try {
      sessionStorage.setItem(_formStateKey(), JSON.stringify(state));
    } catch (e) {
      // sessionStorage unavailable (private browsing, quota exceeded, etc.)
    }
  }

  // Apply saved state back onto the page.  Called twice: once immediately and
  // once after a delay so Select2 is ready for multi-selects.
  function _applyFormState(state) {
    document.querySelectorAll('form').forEach(function (form) {
      if (_isLangForm(form)) return;

      form.querySelectorAll('input, textarea').forEach(function (el) {
        if (!el.name || el.name === 'csrfmiddlewaretoken') return;
        if (el.type === 'file') return;

        if (el.type === 'checkbox' || el.type === 'radio') {
          var key = el.name + '::' + el.value;
          if (key in state._fields) {
            el.checked = state._fields[key];
            el.dispatchEvent(new Event('change', { bubbles: true }));
          }
        } else if (el.name in state._fields) {
          el.value = state._fields[el.name];
          el.dispatchEvent(new Event('input', { bubbles: true }));
        }
      });

      form.querySelectorAll('select').forEach(function (el) {
        if (!el.name || !(el.name in state._selects)) return;
        var saved = state._selects[el.name];
        Array.prototype.forEach.call(el.options, function (opt) {
          opt.selected = saved.indexOf(opt.value) !== -1;
        });
        // Notify Select2 if it is wrapping this element.
        if (typeof $ !== 'undefined' && $.fn.select2 && $(el).data('select2')) {
          $(el).trigger('change.select2');
        } else {
          el.dispatchEvent(new Event('change', { bubbles: true }));
        }
      });
    });
  }

  function initFormStatePersistence() {
    // form.submit() called from onchange does NOT fire the submit event in browsers.
    // We must intercept the change event on the select itself, save state,
    // then let the existing onchange="this.form.submit()" proceed normally.
    // To do that we replace the inline onchange with our own handler that
    // saves first, then submits.
    var langSelect = document.getElementById('lang-switcher');
    if (!langSelect) return;
    var langForm = langSelect.closest('form');
    if (!langForm) return;

    // Remove the inline onchange so our handler is the only one.
    langSelect.removeAttribute('onchange');

    langSelect.addEventListener('change', function () {
      try { _saveFormState(); } catch (e) { /* never block language switch */ }
      // Submit via the button-click path so Django CSRF token is included.
      // form.requestSubmit() fires the submit event; fall back to submit().
      if (typeof langForm.requestSubmit === 'function') {
        langForm.requestSubmit();
      } else {
        langForm.submit();
      }
    });
  }

  function restoreFormState() {
    var key = _formStateKey();
    var raw;
    try { raw = sessionStorage.getItem(key); } catch (e) { return; }
    if (!raw) return;

    // Remove immediately so a normal reload does not re-apply stale data.
    try { sessionStorage.removeItem(key); } catch (e) { /* ignore */ }

    var state;
    try { state = JSON.parse(raw); } catch (e) { return; }
    if (!state || !state._fields) return;

    // First pass: restore plain inputs/textareas right away.
    _applyFormState(state);

    // Second pass (delayed): restore selects after Select2 has initialised.
    // Select2 is loaded in the extra_js block which runs after DOMContentLoaded,
    // so we need to wait for it.
    setTimeout(function () { _applyFormState(state); }, 300);
  }

  // ── Init ─────────────────────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', function () {
    initImagePreview();
    initDependentFields();
    initWorkCurrentToggle();
    initCharCounters();
    initRequiredValidation(); // must come before initSubmitGuard
    initSubmitGuard();
    initCvDropZone();
    initFormStatePersistence();
    restoreFormState();
  });

})();
