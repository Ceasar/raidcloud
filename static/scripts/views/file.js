define(function (require, exports) {
  'use strict';

  var $             = require('jquery')
    , _             = require('underscore')
    , Backbone      = require('backbone')
    , utils         = require('utils');

  exports.FileView = Backbone.View.extend({

    template: utils.template('tmpl-file')

  , render: function () {
      this.$el.html(this.template(this.model.toJSON()));
      this.$el.attr('draggable', 'true');

      return this;
    }

  });

});