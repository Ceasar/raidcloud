define(function (require, exports) {
  'use strict';

  var $           = require('jquery')
    , _           = require('underscore')
    , Backbone    = require('backbone')
    , utils       = require('utils');

  /*
   * Attributes
   * - name
   * - id
   */
  exports.User = Backbone.Model.extend({

    initialize: function () {
      console.log('init user model');
    }

  });

});