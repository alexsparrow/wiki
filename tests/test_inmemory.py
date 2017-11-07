import datetime 
import time
import pytest

from wiki.server import create_web_app
from wiki.inmemory import InMemoryBackend

dummy_data = {
    "doc1": [
        (datetime.datetime.fromtimestamp(0), "foo"),
        (datetime.datetime.fromtimestamp(100), "bar")
    ],
    "doc2": [
        (datetime.datetime.fromtimestamp(100), "a"),
        (datetime.datetime.fromtimestamp(200), "b"),
        (datetime.datetime.fromtimestamp(300), "c")
    ]
}

@pytest.fixture
def cli(loop, test_client):
    app = create_web_app(InMemoryBackend(dummy_data))
    return loop.run_until_complete(test_client(app))

async def test_list_documents(cli):
    resp = await cli.get("/documents")
    assert resp.status == 200
    data = await resp.json()
    assert data == ["doc1", "doc2"]

async def test_list_revisions(cli):
  resp = await cli.get("/documents/doc1")
  assert resp.status == 200
  data = await resp.json()
  assert data == [0, 100]

async def test_missing_document_404(cli):
  resp = await cli.get("/documents/non-existent")
  assert resp.status == 404

async def test_document_at(cli):
  resp = await cli.get("/documents/doc1/0")
  assert resp.status == 404

  resp = await cli.get("/documents/doc1/1")
  assert resp.status == 200
  data = await resp.json()
  assert data == "foo"

  resp = await cli.get("/documents/doc1/101")
  assert resp.status == 200
  data = await resp.json()
  assert data == "bar"

async def test_document_latest(cli):
  resp = await cli.get("/documents/doc1/latest")
  assert resp.status == 200
  data = await resp.json()
  assert data == "bar"

async def test_document_latest_404(cli):
  resp = await cli.get("/documents/doc3/latest")
  assert resp.status == 404

async def test_add(cli):
  resp = await cli.post("/documents/test", json="hello")
  assert resp.status == 200

  resp = await cli.get("/documents/test/latest")
  assert resp.status == 200
  data = await resp.json()
  assert data == "hello"

