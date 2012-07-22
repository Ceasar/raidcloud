define(function (require, exports) {
  'use strict';

  var $           = require('jquery')
    , _           = require('underscore')
    , Backbone    = require('backbone')
    , utils       = require('utils')
    , File        = require('models/file').File;

  exports.FileList = Backbone.Collection.extend({

    model: File

  , initialize: function () {
      console.log('init file list collection');
    }

  , uploadFiles: function (data) {
      var files = data.files
        , that  = this;

      console.log(files);

      _.each(files, function (file) {
        var fileModel = new File(_.extend(file, {
              ownerId: that.options.ownerId
            }));

        fileModel.save();
        that.add(fileModel);
      });
    }

  , setOption: function (option, value) {
      this.options = this.options || {};
      this.options[option] = value;
    }

  });

});