define(function (require, exports) {
  'use strict';

  var $           = require('jquery')
    , _           = require('underscore')
    , Backbone    = require('backbone')
    , utils       = require('utils');

  /*
   * Attributes
   * - owner_id
   * - files
   */
  exports.Finder = Backbone.Model.extend({

    initialize: function () {
      console.log('init finder model');
    }

  , uploadFiles: function (data) {
      // Do ajax request here
    }

  });

});