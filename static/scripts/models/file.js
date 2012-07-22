define(function (require, exports) {
  'use strict';

  var $           = require('jquery')
    , _           = require('underscore')
    , Backbone    = require('backbone')
    , utils       = require('utils');

  exports.File = Backbone.Model.extend({

    defaults: {
      selected: false
    , uploaded: false
    }

  , url: function () {
      var url = '/users/' + this.get('ownerId') + '/files';

      if (!this.isNew()) url += '/' + this.id;

      return url;
    }

  , initialize: function () {
      if (typeof this.get('lastModifiedDate') === 'undefined') {
        this.set('lastModifiedDate', this.get('modified_at'));
      }
    }

  , upload: function () {
      var file = this.get('raw')
        , that = this;

      var xhr = new XMLHttpRequest()
        , data = new FormData();
      data.append('file', file);
      data.append('name', this.get('name'));
      data.append('bytes', file.size);
      data.append('lastModifiedDate', file.lastModifiedDate);

      xhr.file = file;
      xhr.upload.onprogress = function (e) {
        that.onProgress(e, that);
      };
      xhr.onreadystatechange = function (e) {
        that.onStateChange(e, that);
      };
      xhr.open('post', this.url(), true);
      xhr.send(data);
    }

    // Ajax file upload progress event
  , onProgress: function (e, context) {
      var percent = Math.round(e.loaded / e.total);
      $('#progress .bar').css('width', percent + '%');
    }

  , onStateChange: function (e, context) {
      if (e.currentTarget.readyState === 4) {
        context.set('id', e.currentTarget.response.result.id);
        context.set('uploaded', true);
      }
      $('#progress').slideUp();
    }

  });

});