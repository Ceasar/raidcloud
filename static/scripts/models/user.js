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
      , sugarsync: {
          name: 'Sugarsync'
        , url: '/sugarsync'
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
      this.on('change:id', this.initProviders);
    }

  , initProviders: function () {
      var providers = this.get('providers');

      if (this.get('has_dropbox')) {
        providers.dropbox.active = true;
        providers.dropbox.used = Math.round(this.get('dropbox_total') / this.get('dropbox_quota'));
      }
      if (this.get('has_google')) {
        providers.drive.active = true;
        providers.drive.used = Math.round(this.get('drive_total') / this.get('drive_quota'));
      }
      if (this.get('has_box')) {
        providers.box.active = true;
        providers.box.used = Math.round(this.get('box_total') / this.get('box_quota'));
      }
      if (this.get('has_sugarsync')) {
        providers.sugarsync.active = true;
        providers.sugarsync.used = Math.round(this.get('sugarsync_total') / this.get('sugarsync_quota'));
      }
    }

  });

});