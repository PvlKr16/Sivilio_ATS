/**
 * vacancy_select2.js — Select2 initialization for Vacancy form
 * Skills, Working Hours, Working Place, Supervisors
 * HR IT Platform
 */

(function () {
  'use strict';

  if (typeof $ === 'undefined' || !$.fn.select2) return;
  if (!document.getElementById('id_vacancy_skills')) return;

  var common = { theme: 'default', width: '100%', allowClear: true };

  // Skills — multi with search
  $('#id_vacancy_skills').select2($.extend({}, common, {
    placeholder: 'Search and select skills...',
    closeOnSelect: false,
    dropdownParent: $('#id_vacancy_skills').closest('.form-group'),
  }));

  // Working Hours — multi, no search
  $('#id_vacancy_working_hours').select2($.extend({}, common, {
    placeholder: 'Select working hours...',
    closeOnSelect: false,
    minimumResultsForSearch: Infinity,
    dropdownParent: $('#id_vacancy_working_hours').closest('.form-group'),
  }));

  // Working Place — multi, no search
  $('#id_vacancy_working_place').select2($.extend({}, common, {
    placeholder: 'Select working place...',
    closeOnSelect: false,
    minimumResultsForSearch: Infinity,
    dropdownParent: $('#id_vacancy_working_place').closest('.form-group'),
  }));

  // Supervisors — multi with search
  $('#id_vacancy_supervisors').select2($.extend({}, common, {
    placeholder: 'Select supervisors...',
    closeOnSelect: false,
    dropdownParent: $('#id_vacancy_supervisors').closest('.form-group'),
  }));

}());
