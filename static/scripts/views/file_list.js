define(function (require, exports) {
  'use strict';

  var $             = require('jquery')
    , _             = require('underscore')
    , Backbone      = require('backbone')
    , utils         = require('utils')
    , FileView      = require('views/file').FileView;

  exports.FileListView = Backbone.View.extend({

    template: utils.template('tmpl-file-list')

  , events: {
      'drop': 'onFileDrop'
    , 'dragenter': 'onDragEvent'
    , 'dragleave': 'onDragEvent'
    }

  , collectionEvents: {
      'add': 'addFile'
    }

  , render: function () {
      this.$el.html(this.template());

      if (!this.collection.isEmpty()) {
        this.renderFiles();
      }

      return this;
    }

  , renderFiles: function () {
      var $files = this.$('.file-list');

      $files.empty();

      this.collection.each(function (file) {
        var view = new FileView({
              model: file
            });

        $files.append(view.render().$el);
      });
    }

  , addFile: function (file) {
      var $files = this.$('.file-list')
        , view = new FileView({
            model: file
          });

      $files.append(view.render().$el);
    }

  , onDragEvent: function (e) {
      e.stopPropagation();
      e.preventDefault();
      $(e.target).toggleClass('active');
    }

  , onFileDrop: function (e) {
      this.onDragEvent(e);

      if (!e.dataTransfer) e = e.originalEvent;

      this.collection.uploadFiles(e.dataTransfer);
    }

  });

});