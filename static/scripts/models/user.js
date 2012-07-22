define(function (require, exports) {
  'use strict';

  var $           = require('jquery')
    , _           = require('underscore')
    , Backbone    = require('backbone')
    , utils       = require('utils');

  /*
   * Attributes
   * - name
   * - id
   */
  exports.User = Backbone.Model.extend({

    defaults: {
      providers: {
        dropbox: {
          name: 'Dropbox'
        , url: '/dropbox'
        , active: false
        }
      , drive: {
          name: 'Google Drive'
        , url: '/google'
        , active: false
        }
      , box: {
          name: 'Box.net'
        , url: '/box'
        , active: false
        }
      }
    }

  , parse: function (resp) {
      return resp.result;
    }

  , url: function () {
      if (this.isNew()) {
        return '/user';
      } else {
        return '/users/' + this.id;
      }
    }

  , initialize: function () {
      console.log('init user model');

      this.on('change:id', this.initProviders);
    }

  , initProviders: function () {
      if (this.get('dropbox_id')) this.get('providers').dropbox.active = true;
      if (this.get('drive_id')) this.get('providers').drive.active = true;
      if (this.get('box_id')) this.get('providers').box.active = true;
    }

  });

});