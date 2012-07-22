define(function (require, exports) {
  'use strict';

  var $           = require('jquery')
    , _           = require('underscore')
    , Backbone    = require('backbone')
    , utils       = require('utils')
    , File        = require('models/file')
    , User        = require('models/user').User;

  /*
   * Attributes
   * - owner
   * - files
   */
  exports.Finder = Backbone.Model.extend({

    initialize: function () {
      var currentUser = new User()
        , that = this;

      currentUser.fetch({
        success: function (model, response) {
          that.set('owner', model);
        }
      , error: function (model, response) {
          // Redirect to login page
          window.location = '/login';
        }
      });
    }

  });

});