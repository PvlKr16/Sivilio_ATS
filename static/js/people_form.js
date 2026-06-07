/**
 * people_form.js — People form: file-formset add / remove rows
 * Depends on: forms.js (window.HRForms.initDropZone)
 * HR IT Platform
 */

(function () {
  'use strict';

  /* ══════════════════════════════════════════════════════════════════════
     File formset — dynamic add / remove rows
     Requires in the template:
       • #files-rows          — container for formset rows
       • #empty-form-source   — hidden <div> with the empty_form markup
       • #add-file-row        — "Add file" button
       • id_files-TOTAL_FORMS — Django management form input
  ══════════════════════════════════════════════════════════════════════ */

  var PREFIX      = 'files';
  var container   = null;
  var emptySource = null;

  function totalInput() {
    return document.getElementById('id_' + PREFIX + '-TOTAL_FORMS');
  }

  // ── Build a new formset row from the empty_form template ──────────────────
  function buildNewRow(idx) {
    var src = emptySource.cloneNode(true);

    // Patch __prefix__ → real index in all name/id/for attributes
    src.querySelectorAll('[name],[id],[for]').forEach(function (el) {
      ['name', 'id', 'for'].forEach(function (attr) {
        var v = el.getAttribute(attr);
        if (v) el.setAttribute(attr, v.replace(/__prefix__/g, idx));
      });
    });

    // Extract the file <input> Django rendered inside .ef-file
    var fileSpan = src.querySelector('.ef-file');

    // Build drop zone markup
    var dropZone = document.createElement('div');
    dropZone.className = 'cv-drop-zone';
    dropZone.setAttribute('data-drop-zone', '');
    dropZone.innerHTML =
      '<i class="fas fa-file-arrow-up cv-drop-icon"></i>' +
      '<div class="cv-drop-text">Drag &amp; drop PDF here</div>' +
      '<div class="cv-drop-hint">or click to choose</div>' +
      '<div class="cv-drop-filename" style="display:none;"></div>';

    // Wrap the Django file input so initDropZone can find it
    var wrap = document.createElement('span');
    wrap.className = 'cv-drop-input-wrap';
    wrap.appendChild(fileSpan);
    dropZone.appendChild(wrap);

    // Assemble the row
    var row = document.createElement('div');
    row.className = 'file-row mb-3 p-3 border rounded';
    row.style.background = 'var(--color-bg-subtle,#f8f9fa)';
    row.innerHTML =
      '<div class="d-flex gap-3 align-items-center flex-wrap">' +
        '<div style="flex:1;min-width:220px;" class="drop-cell"></div>' +
        '<div>' +
          '<button type="button" class="btn btn-sm btn-outline-danger remove-row" title="Remove">' +
            '<i class="fas fa-times"></i>' +
          '</button>' +
        '</div>' +
      '</div>';

    row.querySelector('.drop-cell').appendChild(dropZone);

    // Append hidden management inputs (TOTAL_FORMS etc.) that cloneNode captured
    src.querySelectorAll('input[type="hidden"]').forEach(function (h) {
      row.appendChild(h);
    });

    return row;
  }

  // ── "Add file" button ─────────────────────────────────────────────────────
  function onAddFileRow() {
    var ti  = totalInput();
    if (!ti) return;
    var idx = parseInt(ti.value, 10);
    var row = buildNewRow(idx);
    container.appendChild(row);
    ti.value = idx + 1;

    // Initialise drag & drop on the freshly created zone
    var zone = row.querySelector('[data-drop-zone]');
    if (zone && window.HRForms && window.HRForms.initDropZone) {
      window.HRForms.initDropZone(zone);
    }
  }

  // ── Remove unsaved row ────────────────────────────────────────────────────
  function onContainerClick(e) {
    var btn = e.target.closest('.remove-row');
    if (btn) btn.closest('.file-row').remove();
  }

  // ── Strike-through when DELETE checkbox is ticked ─────────────────────────
  function onContainerChange(e) {
    if (e.target.type === 'checkbox' &&
        e.target.name &&
        e.target.name.endsWith('-DELETE')) {
      e.target.closest('.file-row').classList.toggle('to-delete', e.target.checked);
    }
  }

  // ── Init ──────────────────────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', function () {
    container   = document.getElementById('files-rows');
    emptySource = document.getElementById('empty-form-source');
    var addBtn  = document.getElementById('add-file-row');

    // Only run on pages that have the files formset
    if (!container || !emptySource || !addBtn) return;

    addBtn.addEventListener('click', onAddFileRow);
    container.addEventListener('click',  onContainerClick);
    container.addEventListener('change', onContainerChange);
  });

}());
