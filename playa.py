import os
import flask
import jinja2
import json
import argparse
import re

app = flask.Flask(__name__)
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('./templates'),
    variable_start_string='[[',
    variable_end_string=']]',
)

def is_music(f):
    return f.lower().endswith('mp3')


@app.route('/m/<path:path>')
def m(path):
    range = flask.request.headers.get('Range')
    length = len(open('/' + path).read())

    if range is None:
        data = open('/' + path).read()
        a, b = 0, len(data)
    else:
        a, b = re.search('bytes=(\d+)-(\d+)', range).groups()
        data = open('/' + path).read()[int(a):int(b)+1]
        
    return flask.Response(
        data,
        206,
        mimetype='audio/mpeg',
        headers={
            'Content-Range': 'bytes {}-{}/{}'.format(a, b, length),
        }
    )

@app.route('/music')
def all_music():
    songs = []
    for dir, dirs, files in os.walk(app.config.music_path):
        for filename in files:
            path = os.path.join(dir, filename)
            if not is_music(path):
                continue
            songs.append({
                'title': unicode(os.path.basename(path), errors='ignore'),
                'path': unicode(path, errors='ignore'),
            })
                        
    data = {
        'songs': sorted(songs, key=lambda x: x['path']),
    }
    return flask.Response(
        json.dumps(data),
        mimetype='application/json',
    )

@app.route('/')
def serve():
    return env.get_template('serve.html').render()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Export music collection.')
    parser.add_argument(
        'music_path', metavar='MUSIC_PATH', type=str,
        help='root of your music collection'
    )

    args = parser.parse_args()
    app.debug = True
    app.config.music_path = args.music_path
    app.run(host='0.0.0.0', port=8000, threaded=True)
