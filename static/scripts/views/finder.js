define(function (require, exports) {
  'use strict';

  var $           = require('jquery')
    , _           = require('underscore')
    , Backbone    = require('backbone')
    , utils       = require('utils');

  exports.FinderView = Backbone.View.extend({

    template: utils.template('tmpl-finder')

  , events: {
      'drop #finder-main': 'onFileDrop'
    , 'dragenter #finder-main': 'onDragenter'
    , 'dragleave #finder-main': 'onDragleave'
    }

  , render: function () {
      var files = this.model.get('files');

      this.$el.html(this.template(this.model.toJSON()));

      if (files && !files.isEmpty()) {
        this.renderFiles();
      }
    }

  , renderFiles: function () {
      var files   = this.model.get('files')
        , $files  = this.$('#file-list');

      $files.empty();

      files.each(function (file) {
        var view = new FileView({
              model: file
            });

        $files.append(view.render().$el);
      });
    }

  , onDragenter: function (e) {
      e.stopPropagation();
      e.preventDefault();
      $(e.target).addClass('active');
    }

  , onDragleave: function (e) {
      e.stopPropagation();
      e.preventDefault();
      $(e.target).removeClass('active');
    }

  , onFileDrop: function (e) {
      e.stopPropagation();
      e.preventDefault();

      console.log(e);
      console.log('file drop');

      this.model.uploadFiles(e.dataTransfer);
    }

  });

});