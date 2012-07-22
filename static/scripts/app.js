/* Javascript entry point for our app */
define(function (require, exports, module) {
  'use strict';

  var $             = require('jquery')
    , _             = require('underscore')
    , Backbone      = require('backbone')
    , utils         = require('utils')
    , Finder        = require('models/finder').Finder
    , FileList      = require('collections/file_list').FileList
    , User          = require('models/user').User
    , FinderView    = require('views/finder').FinderView
    , FileListView  = require('views/file_list').FileListView
    , AccountView   = require('views/account').AccountView;

  require('lib/bootstrap-modal');

  var finder      = new Finder()
    , finderView  = new FinderView({
        model: finder
      , el: $('#app')
      })
    , $finderLinks;

  var init = function () {
    finderView.render();
    finderView.$el.parent().animate({
      'margin-top': 0
    , 'opacity': 1
    }, 500).addClass('show');

    $finderLinks = $('#finder-sidebar a');

    var router = new Router();
    Backbone.history.start({
      pushState: true
    , hashChange: false
    });
  };

  var Router = Backbone.Router.extend({

    routes: {
      '': 'files'
    , 'account': 'account'
    , 'logout': 'logout'
    }

  , files: function () {
      var user          = finder.get('owner')
        , fileList      = new FileList(user.files)
        , fileListView  = new FileListView({
            collection: fileList
          , el: $('#finder-main')
          });

      fileList.setOption('ownerId', finder.get('owner').id);

      $finderLinks.removeClass('selected');
      $finderLinks.eq(0).addClass('selected');

      fileListView.render();
    }

  , account: function () {
      var user = finder.get('owner')
        , accountView = new AccountView({
            model: user
          , el: $('#finder-main')
          });

      console.log('account route');

      $finderLinks.removeClass('selected');
      $finderLinks.eq(1).addClass('selected');

      accountView.render();
    }

  });

  finder.on('change:owner', init);

});