define(function (require, exports) {
  'use strict';

  var $           = require('jquery')
    , _           = require('underscore')
    , Backbone    = require('backbone')
    , utils       = require('utils');

  exports.FinderView = Backbone.View.extend({

    template: utils.template('tmpl-finder')

  , events: {
      'click #finder-sidebar a': 'backboneNavigate'
    }

  , render: function () {
      this.$el.html(this.template(this.model.toJSON()));

      return this;
    }

  , backboneNavigate: function (event) {
      var href = $(event.currentTarget).attr('href');

      // Don't navigate if CTRL, CMD, SHIFT clicked or if href points to an id
      if (!event.altKey && !event.ctrlKey && !event.metaKey && !event.shiftKey && !href.match('#')) {
        event.preventDefault();
        Backbone.history.navigate(href, {trigger: true});
      }
    }

  });

});