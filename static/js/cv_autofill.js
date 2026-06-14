/**
 * cv_autofill.js
 *
 * Handles:
 *  - Single CV file upload (drag&drop or click), PDF only
 *  - Replace / remove before saving
 *  - Sends PDF to /people/parse-cv/ → Claude API
 *  - Autofills person form fields
 *  - Changed fields: black text; unchanged/empty fields: grey placeholder text
 *  - Works for both Create and Edit (existing saved file)
 */

(function () {
  'use strict';

  /* ── Constants ─────────────────────────────────────────────────────────── */

  const PARSE_URL   = document.querySelector('form[data-parse-cv-url]')
                        ?.dataset?.parseCvUrl || '/people/parse-cv/';
  const CSRF_TOKEN  = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';

  // Colour tokens matching your CSS variables
  const COLOR_FILLED  = 'var(--color-text, #212529)';
  const COLOR_EMPTY   = 'var(--color-text-muted, #6c757d)';

  /* ── State ──────────────────────────────────────────────────────────────── */

  let pendingFile    = null;   // File object chosen but not yet saved
  let pendingRemove  = false;  // User wants to delete the existing saved file

  /* ── DOM refs ───────────────────────────────────────────────────────────── */

  const dropZone     = document.getElementById('cv-drop-zone');
  // Django formset renders the file input as id="id_files-0-file"
  const fileInput    = document.getElementById('id_files-0-file') ||
                       document.querySelector('input[name="files-0-file"]');
  const previewWrap  = document.getElementById('cv-preview');
  const previewName  = document.getElementById('cv-preview-name');
  const removeBtn    = document.getElementById('cv-remove-btn');
  const fillBtn      = document.getElementById('cv-fill-btn');
  const fillStatus   = document.getElementById('cv-fill-status');
  const existingWrap = document.getElementById('cv-existing');
  const deleteChk    = document.getElementById('cv-delete-checkbox');  // hidden formset DELETE checkbox
  const actionChoice = document.getElementById('cv-action-choice');
  const btnAnalyse   = document.getElementById('cv-btn-analyse');
  const btnSaveOnly  = document.getElementById('cv-btn-save-only');

  if (!dropZone && !fileInput) return;  // page doesn't have the CV widget

  /* ═══════════════════════════════════════════════════════════════════════════
     FILE SELECTION
  ═══════════════════════════════════════════════════════════════════════════ */

  function onFileChosen(file) {
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.pdf')) {
      showStatus('error', 'Only PDF files are allowed.');
      return;
    }

    pendingFile   = file;
    pendingRemove = false;

    // ── Assign file to the real <input> so browser submits it on form POST ──
    // For drag&drop, fileInput.files is read-only — use DataTransfer to set it
    if (fileInput) {
      try {
        const dt = new DataTransfer();
        dt.items.add(file);
        fileInput.files = dt.files;
      } catch (e) {
        // DataTransfer not supported (very old browsers) — file won't be submitted
        console.warn('DataTransfer not supported:', e);
      }
    }

    // If there was a saved file, mark it for deletion so formset replaces it
    if (deleteChk) deleteChk.checked = true;

    // Show preview
    previewName.textContent = file.name;
    previewWrap.style.display  = 'flex';
    if (existingWrap) existingWrap.style.display = 'none';
    if (dropZone)     dropZone.style.display = 'none';

    clearStatus();

    // Show action choice buttons instead of auto-analysing
    if (actionChoice) actionChoice.style.display = 'block';
  }

  /* ── Input click ────────────────────────────────────────────────────────── */

  if (dropZone) {
    dropZone.addEventListener('click', () => fileInput && fileInput.click());
  }

  if (fileInput) {
    fileInput.addEventListener('change', () => {
      if (fileInput.files[0]) onFileChosen(fileInput.files[0]);
    });
  }

  /* ── Drag & drop ────────────────────────────────────────────────────────── */

  if (dropZone) {
    dropZone.addEventListener('dragover', (e) => {
      e.preventDefault();
      dropZone.classList.add('drag-over');
    });
    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
    dropZone.addEventListener('drop', (e) => {
      e.preventDefault();
      dropZone.classList.remove('drag-over');
      const file = e.dataTransfer?.files?.[0];
      if (file) onFileChosen(file);
    });
  }

  /* ── Action choice buttons ──────────────────────────────────────────────── */

  if (btnAnalyse) {
    btnAnalyse.addEventListener('click', () => {
      if (actionChoice) actionChoice.style.display = 'none';
      if (pendingFile) analyzeCV(pendingFile);
    });
  }

  if (btnSaveOnly) {
    btnSaveOnly.addEventListener('click', () => {
      if (actionChoice) actionChoice.style.display = 'none';
      clearStatus();
    });
  }

  /* ── Remove / replace before save ──────────────────────────────────────── */

  if (removeBtn) {
    removeBtn.addEventListener('click', () => {
      pendingFile = null;

      previewWrap.style.display = 'none';
      if (actionChoice) actionChoice.style.display = 'none';
      clearStatus();

      if (existingWrap) {
        // Editing: restore the saved-file row, uncheck DELETE
        existingWrap.style.display = 'block';
        if (deleteChk) deleteChk.checked = false;
      } else {
        // Creating: show drop zone again
        if (dropZone) dropZone.style.display = 'flex';
      }

      // Reset the real file input so the browser doesn't re-submit the old choice
      if (fileInput) {
        fileInput.value = '';
        try {
          fileInput.files = new DataTransfer().files;
        } catch (e) { /* ignore */ }
      }
    });
  }

  /* ── "Replace" button on existing saved file ────────────────────────────── */

  const replaceBtn = document.getElementById('cv-replace-btn');
  if (replaceBtn) {
    replaceBtn.addEventListener('click', () => {
      if (fileInput) fileInput.click();
    });
  }

  /* ── "Delete saved file" button ─────────────────────────────────────────── */

  const deleteSavedBtn = document.getElementById('cv-delete-saved-btn');
  if (deleteSavedBtn) {
    deleteSavedBtn.addEventListener('click', () => {
      if (deleteChk) deleteChk.checked = true;
      pendingRemove = true;
      if (existingWrap) existingWrap.style.display = 'none';
      if (dropZone)     dropZone.style.display = 'flex';
      clearStatus();
    });
  }

  /* ── Re-analyse button (if user wants to retry) ─────────────────────────── */

  if (fillBtn) {
    fillBtn.addEventListener('click', () => {
      if (pendingFile) analyzeCV(pendingFile);
    });
  }

  /* ═══════════════════════════════════════════════════════════════════════════
     CV ANALYSIS
  ═══════════════════════════════════════════════════════════════════════════ */

  async function analyzeCV(file) {
    showStatus('loading', 'Analysing CV…');
    if (fillBtn) fillBtn.disabled = true;

    const fd = new FormData();
    fd.append('cv_file', file);

    try {
      const resp = await fetch(PARSE_URL, {
        method: 'POST',
        headers: { 'X-CSRFToken': CSRF_TOKEN },
        body: fd,
      });

      const json = await resp.json();

      if (!resp.ok || json.error) {
        showStatus('error', json.error || 'Server error.');
        return;
      }

      fillForm(json.data);
      showStatus('success', 'Form filled from CV. Review and save.');

    } catch (err) {
      showStatus('error', 'Network error. Please try again.');
      console.error('CV parse error:', err);
    } finally {
      if (fillBtn) fillBtn.disabled = false;
    }
  }

  /* ═══════════════════════════════════════════════════════════════════════════
     FORM FILL
  ═══════════════════════════════════════════════════════════════════════════ */

  function fillForm(data) {
    // ── Simple text / number inputs ────────────────────────────────────────
    const textFields = [
      'first_name', 'last_name', 'email', 'phone',
      'telegram', 'linkedin', 'profession', 'education',
      'work_experience', 'salary_desired',
    ];

    textFields.forEach((name) => {
      const el = document.querySelector(`[name="${name}"]`);
      if (!el) return;
      const val = data[name];
      if (val !== null && val !== undefined && val !== '') {
        el.value = String(val);
        markChanged(el);
      } else {
        markUnchanged(el);
      }
    });

    // ── Select fields ──────────────────────────────────────────────────────
    const selectFields = [
      { name: 'level',    key: 'level_id' },
      { name: 'english',  key: 'english_id' },
      { name: 'region',   key: 'region_id' },
      { name: 'salary_currency', key: 'salary_currency' },
    ];

    selectFields.forEach(({ name, key }) => {
      const el = document.getElementById(`id_${name}`) ||
                 document.querySelector(`[name="${name}"]`);
      if (!el) return;
      const val = data[key] ?? data[name];
      if (val !== null && val !== undefined && val !== '') {
        el.value = String(val);
        if (el.value === String(val)) {
          markChanged(el);
          // Trigger Select2 refresh if present
          if (window.$ && $(el).data('select2')) {
            $(el).trigger('change.select2');
          }
        }
      } else {
        markUnchanged(el);
      }
    });

    // ── Skills (Select2 multiple) ──────────────────────────────────────────
    const skillIds = data.skill_ids;
    const skillsSelect = document.getElementById('id_skills_select2');
    if (skillsSelect && Array.isArray(skillIds) && skillIds.length > 0) {
      const strIds = skillIds.map(String);
      Array.from(skillsSelect.options).forEach((opt) => {
        opt.selected = strIds.includes(opt.value);
      });
      if (window.$ && $(skillsSelect).data('select2')) {
        $(skillsSelect).trigger('change.select2');
      }
      markChanged(skillsSelect);
    }
  }

  /* ═══════════════════════════════════════════════════════════════════════════
     VISUAL STATE: changed vs unchanged
  ═══════════════════════════════════════════════════════════════════════════ */

  function markChanged(el) {
    el.style.color = COLOR_FILLED;
    el.classList.add('cv-autofilled');
    el.classList.remove('cv-unfilled');
  }

  function markUnchanged(el) {
    // Only apply grey hint if the field is actually empty
    if (!el.value || el.value === '' || el.value === '0') {
      el.style.color = COLOR_EMPTY;
      el.classList.add('cv-unfilled');
      el.classList.remove('cv-autofilled');
    }
  }

  // When the user manually edits a grey field, restore black text
  document.addEventListener('input', (e) => {
    const el = e.target;
    if (el.classList.contains('cv-unfilled') && el.value) {
      markChanged(el);
    }
  });
  document.addEventListener('change', (e) => {
    const el = e.target;
    if (el.classList.contains('cv-unfilled') && el.value) {
      markChanged(el);
    }
  });

  /* ═══════════════════════════════════════════════════════════════════════════
     STATUS MESSAGES
  ═══════════════════════════════════════════════════════════════════════════ */

  function showStatus(type, text) {
    if (!fillStatus) return;
    fillStatus.className = `cv-fill-status cv-fill-status--${type}`;
    if (type === 'loading') {
      fillStatus.innerHTML = `<span class="cv-spinner"></span>${text}`;
    } else {
      fillStatus.textContent = text;
    }
    fillStatus.style.display = 'block';
  }

  function clearStatus() {
    if (!fillStatus) return;
    fillStatus.style.display = 'none';
    fillStatus.textContent   = '';
    fillStatus.className     = 'cv-fill-status';
  }

})();