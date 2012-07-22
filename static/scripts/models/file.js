define(funciton (require, exports) {
  'use strict';

  var $           = require('jquery')
    , _           = require('underscore')
    , Backbone    = require('backbone')
    , utils       = require('utils');

  exports.File = Backbone.Model.extend({

    initialize: function () {
      console.log('init file model');
    }

  });

});