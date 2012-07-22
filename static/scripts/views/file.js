define(function (require, exports) {
  'use strict';

  var $             = require('jquery')
    , _             = require('underscore')
    , Backbone      = require('backbone')
    , utils         = require('utils');

  exports.FileView = Backbone.View.extend({

    tagName: 'a'

  , className: 'file'

  , template: utils.template('tmpl-file')

  , events: {
      'click': 'select'
    , 'click .delete': 'delete'
    }

  , render: function () {
      var model = (this.model.get('raw')) ? this.model.get('raw') : this.model.toJSON();

      this.$el.html(this.template(model));
      this.$el.attr('draggable', 'true');

      return this;
    }

  , select: function (e) {
      e.preventDefault();
      e.stopPropagation();

      this.$el.toggleClass('selected');
      this.model.set('selected', !this.model.get('selected'));
    }

  , delete: function (e) {
      e.preventDefault();
      e.stopPropagation();

      var collection = this.model.collection;

      this.model.destroy();
      collection.trigger('removeFile');
    }

  });

});