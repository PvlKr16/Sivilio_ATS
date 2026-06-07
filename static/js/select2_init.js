/**
 * select2_init.js — Select2 initialization for People form
 * Handles: Skills (multi + search), Working Hours (multi), Working Place (multi)
 * Main Skill uses the native <select> — NOT initialized with Select2
 * HR IT Platform
 */

(function () {
  'use strict';

  // Only run on pages that have the skills select
  if (typeof $ === 'undefined' || !$.fn.select2) return;
  if (!document.getElementById('id_skills_select2')) return;

  var commonConfig = {
    theme: 'default',
    width: '100%',
    allowClear: true,
  };

  // Skills — multi-select with search
  $('#id_skills_select2').select2($.extend({}, commonConfig, {
  placeholder: $('#id_skills_select2').data('placeholder'),
  closeOnSelect: false,
  dropdownParent: $('#id_skills_select2').closest('.form-group'),
  }));

  // Working Hours — multi, no search (short list)
  $("#id_working_hours_select2").select2($.extend({}, commonConfig, {
    placeholder: $("#id_working_hours_select2").data('placeholder'),
    closeOnSelect: false,
    minimumResultsForSearch: Infinity,
    dropdownParent: $('#id_working_hours_select2').closest('.form-group'),
  }));

  // Working Place — multi, no search (short list)
  $('#id_working_place_select2').select2($.extend({}, commonConfig, {
    placeholder: $('#id_working_place_select2').data('placeholder'),
    closeOnSelect: false,
    minimumResultsForSearch: Infinity,
    dropdownParent: $('#id_working_place_select2').closest('.form-group'),
  }));

  // Explicitly destroy any accidental Select2 on main_skill and other native selects
  ['id_main_skill', 'id_profession', 'id_level', 'id_english',
   'id_gender', 'id_region', 'id_status', 'id_salary_currency'].forEach(function (id) {
    var el = document.getElementById(id);
    if (el && $(el).data('select2')) {
      $(el).select2('destroy');
    }
  });

}());
