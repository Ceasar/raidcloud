define(function (require, exports) {
  'use strict';

  var $           = require('lib/jquery')
    , _           = require('lib/underscore.min');

  var utils = {

    // Returns a function that renders an underscore template given its DOM id
    template: function (domId) {
      return _.template(($('#' + domId).html() || '').trim());
    }

  };

  exports = utils;

});