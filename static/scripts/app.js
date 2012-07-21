/* Javascript entry point for our app */
define(function (require) {
  'use strict';

  var $           = require('lib/jquery')
    , _           = require('lib/underscore.min')
    , Backbone    = require('lib/backbone.min')
    , utils       = require('utils');

  require('lib/bootstrap-modal');

  console.log('init');

  var AppModel = Backbone.Model.extend({

  });

  var AppView = Backbone.View.extend({

    events: {

    }

  , template: utils.template('tmpl-main')

  , initialize: function () {

    }

  , render: function () {
      this.$el.html(this.template(this.model.toJSON()));
    }

  });


  var Router = Backbone.Router.extend({

    routes: {
      '/app': 'app'
    }

  , app: function () {
      var appModel = new AppModel()
        , appView  = new AppView({
            model: appModel
          , el: $('#main')
          });

      appView.render();
    }

  });

  var router = new Router();
  Backbone.history.start({
    pushState: true
  , hashChange: false
  });

});