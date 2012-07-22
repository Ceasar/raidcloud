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
    , 'click #delete-all a': 'deleteSelected'
    }

  , collectionEvents: {
      'add': 'addFile'
    , 'removeFile': 'renderFiles'
    , 'change:selected': 'onSelect'
    }

  , initialize: function () {
      this.state = {
        deleting: false
      };
    }

  , render: function () {
      this.$el.html(this.template());

      if (!this.collection.isEmpty()) {
        this.renderFiles();
      }

      return this;
    }

  , renderFiles: function (force) {
      var $files = this.$('.file-list');

      $files.empty();

      if (this.collection.isEmpty()) {
        this.$('.no-files').fadeIn();
      } else {
        this.collection.each(function (file) {
          var view = new FileView({
                model: file
              });

          $files.append(view.render().$el);
        });
      }
    }

  , addFile: function (file) {
      var $files    = this.$('.file-list')
        , $noFiles  = this.$('.no-files')
        , view = new FileView({
            model: file
          });

      if ($noFiles.is(':visible')) $noFiles.slideUp('fast');

      $files.append(view.render().$el);
    }

  , onSelect: function (e) {
      var anySelected = _.any(this.collection.pluck('selected'))
        , $del = this.$('#delete-all');

      if (anySelected) {
        $del.slideDown('fast');
      } else {
        $del.slideUp('fast');
      }
    }

  , deleteSelected: function (e) {
      var length = this.collection.length;

      for (var i = 0; i < length; i++) {
        var file = this.collection.at(i);
        if (file && file.get('selected')) file.destroy();
      }

      this.collection.trigger('removeFile');

      this.$('#delete-all').slideUp('fast');
    }

  , onFileDrop: function (e) {
      e.stopPropagation();
      e.preventDefault();
      $(e.currentTarget).toggleClass('active');

      if (!e.dataTransfer) e = e.originalEvent;

      this.collection.uploadFiles(e.dataTransfer);

      this.$('#progress').slideDown('fast');
    }

  });

});