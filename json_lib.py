from flask import json, request, app, Response
import datetime
import dateutil.parser
from dateutil.tz import *

class JSONEncoder(json.JSONEncoder):
    '''JSONEncoder that supports datetime serialization into iso8601.'''

    def default(self, obj):
        if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)

def as_date(dct):
    '''simplejson loads object_hook that deserializes datetimes.

    Any value for a property with a name ending in '_at' will be
    deserialized to from iso8601 format to a python datetime. If there is no
    timezone information in the iso8601 date string, the UTC timezone is
    assumed.

    '''
    for k in dct:
        if k.endswith(('_at', '_date')):
            if dct[k] is not None:
                date = dateutil.parser.parse(dct[k])

                if date.tzinfo is None:
                    date = date.replace(tzinfo=tzutc())

                dct[k] = date
    return dct

def loads(json_string, **kwargs):
    '''Our own version of loads that automatically uses the 'as_date' hook'''

    return json.loads(json_string, object_hook=as_date, **kwargs)

def dumps(*args, **kwargs):
    return json.dumps(dict(*args, **kwargs), indent=None, cls=JSONEncoder)

def jsonify(*args, **kwargs):
    '''Our own version of flask's jsonify that uses our JSONEncoder.

    Flask jsonify docstring follows:

    Creates a :class:`~flask.Response` with the JSON representation of
    the given arguments with an `application/json` mimetype.  The arguments
    to this function are the same as to the :class:`dict` constructor.

    Example usage::

        @app.route('/_get_current_user')
        def get_current_user():
            return jsonify(username=g.user.username,
                           email=g.user.email,
                           id=g.user.id)

    This will send a JSON response like this to the browser::

        {
            "username": "admin",
            "email": "admin@localhost",
            "id": 42
        }

    This requires Python 2.6 or an installed version of simplejson.  For
    security reasons only objects are supported toplevel.  For more
    information about this, have a look at :ref:`json-security`.

    .. versionadded:: 0.2

    .. versionadded:: 0.9
        If the ``padded`` argument is true, the JSON object will be padded
        for JSONP calls and the response mimetype will be changed to 
        ``application/javascript``. By default, the request arguments ``callback``
        and ``jsonp`` will be used as the name for the callback function.
        This will work with jQuery and most other JavaScript libraries
        by default.

        If the ``padded`` argument is a string, jsonify will look for
        the request argument with the same name and use that value as the
        callback-function name.
    '''

    try:
        result_obj = dict(*args, **kwargs)
    except ValueError:
        result_obj = args[0]

    if 'padded' in kwargs:
        if isinstance(kwargs['padded'], str):
            callback = request.args.get(kwargs['padded']) or 'jsonp'
        else:
            callback = request.args.get('callback') or \
                       request.args.get('jsonp') or 'jsonp'
        del kwargs['padded']
        json_str = dumps({'result': result_obj})
        content = str(callback) + "(" + json_str + ")"
        return current_app.response_class(content, mimetype='application/javascript')
    return Response(response=json.dumps({'result': result_obj},
        indent=2, cls=JSONEncoder), mimetype='application/json')
