define(function (require, exports) {
  'use strict';

  var $           = require('jquery')
    , _           = require('underscore')
    , Backbone    = require('backbone')
    , utils       = require('utils')
    , File        = require('models/file').File;

  exports.FileList = Backbone.Collection.extend({

    model: File

  , uploadFiles: function (data) {
      var files = data.files
        , that  = this;

      _.each(files, function (file) {
        var fileModel = new File({
              ownerId: that.options.ownerId
            , raw: file
            , name: file.name
            });

        fileModel.upload();
        that.add(fileModel);
      });
    }

  , setOwnerId: function (ownerId) {
      this.options = this.options || {};
      this.options.ownerId = ownerId;

      _.each(this.models, function (file) {
        file.set('ownerId', ownerId);
      });
    }

  });

});