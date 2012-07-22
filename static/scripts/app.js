/* Javascript entry point for our app */
define(function (require, exports, module) {
  'use strict';

  var $           = require('jquery')
    , _           = require('underscore')
    , Backbone    = require('backbone')
    , utils       = require('utils')
    , Finder      = require('models/finder').Finder
    , User        = require('models/user').User
    , FinderView  = require('views/finder').FinderView
    , AccountView = require('views/account').AccountView;

  require('lib/bootstrap-modal');

  var Router = Backbone.Router.extend({

    routes: {
      'files': 'files'
    , 'account': 'account'
    , 'logout': 'logout'
    }

  , files: function () {
      var fileList      = new FileList()
        , fileListView  = new FileListView({
            collection: fileList
          , el: $('#finder-main')
          });

      console.log('files route');
      fileListView.render();
    }

  , account: function () {
      var user = new User({
            name: 'Current User'
          })
        , accountView = new AccountView({
            model: user
          , el: $('#finder-main')
          });

      console.log('account route');
      accountView.render();
    }

  });

  var finder      = new Finder()
    , finderView  = new FinderView({
        model: finder
      , el: $('#app')
      });
  finderView.render();

  var router = new Router();
  Backbone.history.start({
    pushState: true
  , hashChange: false
  });

});