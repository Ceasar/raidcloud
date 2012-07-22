define(function (require, exports) {
  'use strict';

  var $             = require('jquery')
    , _             = require('underscore')
    , Backbone      = require('backbone')
    , utils         = require('utils');

  exports.AccountView = Backbone.View.extend({

    template: utils.template('tmpl-account')

  , render: function () {
      this.$el.html(this.template(this.model.toJSON()));

      return this;
    }

  });

});