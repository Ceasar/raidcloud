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
    , 'dragenter #finder-main': 'onDragEvent'
    , 'dragleave #finder-main': 'onDragEvent'
    }

  , render: function () {
      this.$el.html(this.template(this.model.toJSON()));

      return this;
    }

  , onDragEvent: function (e) {
      e.stopPropagation();
      e.preventDefault();
      $(e.currentTarget).toggleClass('active');
    }

  , backboneNavigate: function (event) {
      var href = $(event.currentTarget).attr('href');

      // Don't navigate if CTRL, CMD, SHIFT clicked or if href points to logout
      if (!event.altKey && !event.ctrlKey && !event.metaKey && !event.shiftKey && !href.match('logout')) {
        event.preventDefault();
        Backbone.history.navigate(href, {trigger: true});
      }
    }

  });

});