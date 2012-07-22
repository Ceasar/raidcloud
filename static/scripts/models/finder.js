define(function (require, exports) {
  'use strict';

  var $           = require('jquery')
    , _           = require('underscore')
    , Backbone    = require('backbone')
    , utils       = require('utils')
    , File        = require('models/file')
    , User        = require('models/user');

  /*
   * Attributes
   * - owner
   * - files
   */
  exports.Finder = Backbone.Model.extend({

    initialize: function () {
      console.log('init finder model');

      $.get('/user', function (resp) {
        var currentUser = new User(resp);
        this.set('owner', currentUser)
      });
    }

  });

});