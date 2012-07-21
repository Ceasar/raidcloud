/* Javascript entry point for our app */
define(function (require, exports, module) {
  'use strict';

  var $           = require('jquery')
    , _           = require('underscore')
    , Backbone    = require('backbone')
    , utils       = require('utils');

  require('lib/bootstrap-modal');

  var AppModel = Backbone.Model.extend({

    initialize: function () {
      console.log('init model');
    }

  });

  var AppView = Backbone.View.extend({

    template: utils.template('tmpl-main')

  , render: function () {
      this.$el.html(this.template(this.model.toJSON()));
    }

  });

  var Router = Backbone.Router.extend({

    routes: {
      '': 'app'
    }

  , app: function () {
      var appModel = new AppModel()
        , appView  = new AppView({
            model: appModel
          , el: $('#main')
          });

      console.log('app route');
      appView.render();
    }

  });

  var router = new Router();
  Backbone.history.start({
    pushState: true
  , hashChange: false
  });

});