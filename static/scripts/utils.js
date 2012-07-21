define(function (require, exports, module) {
  'use strict';

  var $           = require('jquery')
    , _           = require('underscore');

  var utils = {

    // Returns a function that renders an underscore template given its DOM id
    template: function (domId) {
      return _.template(($('#' + domId).html() || '').trim());
    }

  };

  module.exports = utils;

});