/**
 * tables.js — Data table helpers
 * Client-side column sort, live search highlight, row actions
 * HR IT Platform
 */

(function () {
  'use strict';

  // ── Live search highlight in table rows ───────────────────────────────────
  function initTableSearch() {
    document.querySelectorAll('[data-table-search]').forEach(function (input) {
      var tableId = input.dataset.tableSearch;
      var table   = document.getElementById(tableId);
      if (!table) return;

      var rows = Array.from(table.querySelectorAll('tbody tr'));

      input.addEventListener('input', function () {
        var query = this.value.toLowerCase().trim();
        rows.forEach(function (row) {
          var text = row.textContent.toLowerCase();
          row.style.display = (!query || text.includes(query)) ? '' : 'none';
        });
        var noResults = table.querySelector('.no-results-row');
        if (noResults) {
          var visible = rows.filter(function (r) { return r.style.display !== 'none'; });
          noResults.style.display = visible.length === 0 ? '' : 'none';
        }
      });
    });
  }

  // ── Client-side column sort ───────────────────────────────────────────────
  function initColumnSort() {
    document.querySelectorAll('table.data-table').forEach(function (table) {
      var headers = table.querySelectorAll('th[data-sortable]');
      if (!headers.length) return;

      headers.forEach(function (th) {
        th.style.cursor = 'pointer';
        th.style.userSelect = 'none';

        var indicator = document.createElement('span');
        indicator.className = 'sort-indicator';
        indicator.innerHTML = ' <i class="fas fa-sort" style="opacity:.3;font-size:10px"></i>';
        th.appendChild(indicator);

        var ascending = true;

        th.addEventListener('click', function () {
          var tbody     = table.querySelector('tbody');
          var rows      = Array.from(tbody.querySelectorAll('tr'));
          var allThs    = Array.from(table.querySelectorAll('thead th'));
          var realIndex = allThs.indexOf(th);

          rows.sort(function (a, b) {
            var aText = (a.cells[realIndex] ? a.cells[realIndex].textContent : '').trim().toLowerCase();
            var bText = (b.cells[realIndex] ? b.cells[realIndex].textContent : '').trim().toLowerCase();
            var aNum  = parseFloat(aText);
            var bNum  = parseFloat(bText);
            if (!isNaN(aNum) && !isNaN(bNum)) return ascending ? aNum - bNum : bNum - aNum;
            return ascending ? aText.localeCompare(bText) : bText.localeCompare(aText);
          });

          rows.forEach(function (r) { tbody.appendChild(r); });

          headers.forEach(function (h) {
            h.querySelector('.sort-indicator i').className = 'fas fa-sort';
            h.querySelector('.sort-indicator i').style.opacity = '.3';
          });
          indicator.querySelector('i').className = ascending ? 'fas fa-sort-up' : 'fas fa-sort-down';
          indicator.querySelector('i').style.opacity = '1';
          ascending = !ascending;
        });
      });
    });
  }

  // ── Row click navigation ──────────────────────────────────────────────────
  function initRowNavigation() {
    document.querySelectorAll('tr[data-href]').forEach(function (row) {
      row.style.cursor = 'pointer';
      row.addEventListener('click', function (e) {
        if (e.target.closest('a, button, .btn')) return;
        window.location.href = this.dataset.href;
      });
    });
  }

  // ── Multi-select dropdown widget ─────────────────────────────────────────
  //
  // Strategy:
  // 1. Read options + initial checked state from the hidden Django
  //    CheckboxSelectMultiple in #ms-source-data [data-ms-for="{name}"].
  //    Django sets cb.checked correctly from request.GET on the server,
  //    so this is always the source of truth after a page load.
  //
  // 2. For each field, maintain a set of persistent <input type="hidden">
  //    elements directly inside the <form>. These are created once and
  //    kept in sync with the selection on every checkbox change.
  //    No submit-listener magic — the hidden inputs are always there.
  //
  // 3. The dropdown is appended to <body> (position:fixed) so it is never
  //    clipped by overflow:hidden on ancestor cards.
  //
  // 4. The #ms-source-data container must be OUTSIDE the <form> so its
  //    checkboxes are never submitted along with the hidden inputs.

  function buildMultiSelect(wrap) {
    var name        = wrap.dataset.name;
    var placeholder = wrap.dataset.placeholder || name;

    // ── 1. Read options from hidden Django widget ─────────────────────────
    var sourceDiv = document.querySelector('[data-ms-for="' + name + '"]');
    var options   = [];
    if (sourceDiv) {
      sourceDiv.querySelectorAll('input[type=checkbox]').forEach(function (cb) {
        var label = cb.closest('label') || cb.parentElement;
        options.push({
          value:    cb.value,
          label:    label ? label.textContent.trim() : cb.value,
          selected: cb.checked,   // Django sets this from request.GET
        });
      });
    }

    // ── 2. Create persistent hidden inputs inside the form ────────────────
    var form = wrap.closest('form');

    function syncHiddenInputs() {
      if (!form) return;
      // Remove old ones for this field
      form.querySelectorAll('input[type=hidden][data-ms="' + name + '"]')
          .forEach(function (el) { el.remove(); });
      // Add one per selected option
      options.filter(function (o) { return o.selected; }).forEach(function (opt) {
        var h = document.createElement('input');
        h.type  = 'hidden';
        h.name  = name;
        h.value = opt.value;
        h.setAttribute('data-ms', name);
        form.appendChild(h);
      });
    }

    // Sync immediately so initial state (from Django) is in the form
    syncHiddenInputs();

    // ── 3. Build trigger button ───────────────────────────────────────────
    var trigger = document.createElement('div');
    trigger.className = 'ms-trigger';
    trigger.setAttribute('role', 'button');
    trigger.setAttribute('tabindex', '0');
    trigger.innerHTML =
      '<span class="ms-label">' + placeholder + '</span>' +
      '<span class="ms-badge" style="display:none"></span>' +
      '<i class="fas fa-chevron-down ms-arrow"></i>';
    wrap.appendChild(trigger);

    // ── 4. Build dropdown (appended to body, position:fixed) ──────────────
    var dropdown = document.createElement('div');
    dropdown.className = 'ms-dropdown';
    dropdown.style.display = 'none';
    dropdown.addEventListener('mousedown', function (e) { e.stopPropagation(); });
    dropdown.addEventListener('click',     function (e) { e.stopPropagation(); });
    document.body.appendChild(dropdown);

    // Search box (only when >= 6 options)
    var searchInput = null;
    if (options.length >= 6) {
      var searchDiv = document.createElement('div');
      searchDiv.className = 'ms-search';
      searchInput = document.createElement('input');
      searchInput.type        = 'text';
      searchInput.placeholder = 'Search\u2026';
      searchDiv.appendChild(searchInput);
      dropdown.appendChild(searchDiv);
    }

    var list = document.createElement('div');
    list.className = 'ms-list';
    dropdown.appendChild(list);

    // ── Helpers ───────────────────────────────────────────────────────────
    function positionDropdown() {
      var rect = wrap.getBoundingClientRect();
      dropdown.style.top      = (rect.bottom + 4) + 'px';
      dropdown.style.left     = rect.left + 'px';
      dropdown.style.minWidth = rect.width + 'px';
    }

    function renderItems(filter) {
      list.innerHTML = '';
      var visible = 0;
      options.forEach(function (opt) {
        if (filter && opt.label.toLowerCase().indexOf(filter.toLowerCase()) === -1) return;
        visible++;
        var item = document.createElement('label');
        item.className = 'ms-item';

        var cb = document.createElement('input');
        cb.type    = 'checkbox';
        cb.value   = opt.value;
        cb.checked = opt.selected;
        cb.addEventListener('change', function () {
          opt.selected = cb.checked;
          syncHiddenInputs();   // keep form in sync immediately
          updateTrigger();
        });

        item.appendChild(cb);
        item.appendChild(document.createTextNode(opt.label));
        list.appendChild(item);
      });

      if (visible === 0) {
        var empty = document.createElement('div');
        empty.className = 'ms-empty';
        empty.textContent = 'No options found.';
        list.appendChild(empty);
      }
    }

    function updateTrigger() {
      var selected = options.filter(function (o) { return o.selected; });
      var labelEl  = trigger.querySelector('.ms-label');
      var badgeEl  = trigger.querySelector('.ms-badge');

      if (selected.length === 0) {
        labelEl.textContent = placeholder;
        labelEl.classList.remove('has-value');
        badgeEl.style.display = 'none';
      } else if (selected.length === 1) {
        labelEl.textContent = selected[0].label;
        labelEl.classList.add('has-value');
        badgeEl.style.display = 'none';
      } else {
        labelEl.textContent = placeholder;
        labelEl.classList.add('has-value');
        badgeEl.style.display = '';
        badgeEl.textContent   = selected.length;
      }
    }

    function closeAll() {
      document.querySelectorAll('.ms-wrap.open').forEach(function (w) {
        w.classList.remove('open');
        if (w._msDropdown) w._msDropdown.style.display = 'none';
      });
    }

    function openDropdown() {
      var isOpen = wrap.classList.contains('open');
      closeAll();
      if (!isOpen) {
        wrap.classList.add('open');
        positionDropdown();
        dropdown.style.display = 'block';
        if (searchInput) {
          searchInput.value = '';
          renderItems('');
          searchInput.focus();
        }
      }
    }

    wrap._msDropdown = dropdown;

    trigger.addEventListener('click', function (e) {
      e.stopPropagation();
      openDropdown();
    });
    trigger.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openDropdown(); }
      if (e.key === 'Escape') {
        wrap.classList.remove('open');
        dropdown.style.display = 'none';
      }
    });

    if (searchInput) {
      searchInput.addEventListener('input', function () { renderItems(this.value); });
    }

    window.addEventListener('scroll', function () {
      if (wrap.classList.contains('open')) positionDropdown();
    }, { passive: true });
    window.addEventListener('resize', function () {
      if (wrap.classList.contains('open')) positionDropdown();
    }, { passive: true });

    // Initial render
    renderItems('');
    updateTrigger();
  }

  function initMultiSelects() {
    document.addEventListener('mousedown', function () {
      document.querySelectorAll('.ms-wrap.open').forEach(function (w) {
        w.classList.remove('open');
        if (w._msDropdown) w._msDropdown.style.display = 'none';
      });
    });

    document.querySelectorAll('.ms-wrap[data-name]').forEach(buildMultiSelect);
  }

  // ── Init on DOM ready ─────────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', function () {
    initTableSearch();
    initColumnSort();
    initRowNavigation();
    initMultiSelects();
  });

})();