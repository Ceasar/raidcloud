define(function (require, exports) {
  'use strict';

  var $           = require('jquery')
    , _           = require('underscore')
    , Backbone    = require('backbone')
    , utils       = require('utils');

  exports.File = Backbone.Model.extend({

    url: function () {
      var url = '/users/' + this.get('ownerId');

      if (!this.isNew()) url += this.get('id');

      return url;
    }

  , initialize: function () {
      console.log('init file model');
    }

  });

});