import json

from app import app


def test_root_service_worker_is_served_with_javascript_mime_type():
    response = app.test_client().get('/service-worker.js')

    assert response.status_code == 200
    assert response.mimetype == 'application/javascript'
    assert b"'/templates/index.html'" not in response.data
    assert b"pathname.startsWith('/api/')" in response.data


def test_manifest_icons_are_available():
    client = app.test_client()
    manifest_response = client.get('/static/manifest.json')
    manifest = json.loads(manifest_response.data)

    assert manifest_response.status_code == 200
    for icon in manifest['icons']:
        icon_response = client.get(icon['src'])
        assert icon_response.status_code == 200
        assert icon_response.mimetype == 'image/svg+xml'


def test_home_registers_root_scoped_service_worker():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert b"navigator.serviceWorker.register('/service-worker.js')" in response.data