/**
 * tables.js — Data table helpers
 * Client-side column sort, live search highlight, row actions
 * HR IT Platform
 */

(function () {
  'use strict';

  // ── Live search highlight in table rows ───────────────────────────────────
  // Attach to any input with [data-table-search="<tableId>"]
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

        // Show/hide empty state row if present
        var noResults = table.querySelector('.no-results-row');
        if (noResults) {
          var visible = rows.filter(function (r) { return r.style.display !== 'none'; });
          noResults.style.display = visible.length === 0 ? '' : 'none';
        }
      });
    });
  }

  // ── Client-side column sort ───────────────────────────────────────────────
  // Add data-sortable to <th> elements to make them clickable
  function initColumnSort() {
    document.querySelectorAll('table.data-table').forEach(function (table) {
      var headers = table.querySelectorAll('th[data-sortable]');
      if (!headers.length) return;

      headers.forEach(function (th, colIndex) {
        th.style.cursor = 'pointer';
        th.style.userSelect = 'none';

        // Add sort indicator
        var indicator = document.createElement('span');
        indicator.className = 'sort-indicator';
        indicator.innerHTML = ' <i class="fas fa-sort" style="opacity:.3;font-size:10px"></i>';
        th.appendChild(indicator);

        var ascending = true;

        th.addEventListener('click', function () {
          var tbody = table.querySelector('tbody');
          var rows  = Array.from(tbody.querySelectorAll('tr'));

          // Get the actual column index in the table (account for preceding non-sortable cols)
          var allThs   = Array.from(table.querySelectorAll('thead th'));
          var realIndex = allThs.indexOf(th);

          rows.sort(function (a, b) {
            var aText = (a.cells[realIndex] ? a.cells[realIndex].textContent : '').trim().toLowerCase();
            var bText = (b.cells[realIndex] ? b.cells[realIndex].textContent : '').trim().toLowerCase();
            var aNum  = parseFloat(aText);
            var bNum  = parseFloat(bText);

            if (!isNaN(aNum) && !isNaN(bNum)) {
              return ascending ? aNum - bNum : bNum - aNum;
            }
            return ascending
              ? aText.localeCompare(bText)
              : bText.localeCompare(aText);
          });

          rows.forEach(function (r) { tbody.appendChild(r); });

          // Update all indicators in this table
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
  // Rows with [data-href] navigate on click (like a link)
  function initRowNavigation() {
    document.querySelectorAll('tr[data-href]').forEach(function (row) {
      row.style.cursor = 'pointer';
      row.addEventListener('click', function (e) {
        // Don't navigate if user clicked an action button inside the row
        if (e.target.closest('a, button, .btn')) return;
        window.location.href = this.dataset.href;
      });
    });
  }

  // ── Init on DOM ready ─────────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', function () {
    initTableSearch();
    initColumnSort();
    initRowNavigation();
  });

})();
