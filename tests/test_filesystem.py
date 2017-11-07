import datetime 
import time
import pytest

from wiki.server import create_web_app
from wiki.filesystem import FileSystemBackend

@pytest.fixture
def cli(loop, test_client, tmpdir_factory):
    app = create_web_app(FileSystemBackend(tmpdir_factory.mktemp("data"), loop))
    return loop.run_until_complete(test_client(app))

async def test_latest(cli):
  resp = await cli.post("/documents/test", json="hello")
  assert resp.status == 200

  resp = await cli.get("/documents/test/latest")
  assert resp.status == 200
  data = await resp.json()
  assert data == "hello"

async def test_documents(cli):
  resp = await cli.post("/documents/test1", json="hello")
  resp = await cli.post("/documents/test2", json="goodbye")

  resp = await cli.get("/documents")
  assert resp.status == 200
  data = await resp.json()
  assert set(data) == set(["test1", "test2"])

async def test_revisions(cli):
  resp = await cli.post("/documents/test", json="hello")
  assert resp.status == 200

  resp = await cli.post("/documents/test", json="goodbye")
  assert resp.status == 200

  resp = await cli.get("/documents/test")
  data = await resp.json()
  assert len(data) == 2

  resp = await cli.get("/documents/test/latest")
  assert resp.status == 200
  data = await resp.json()
  assert data == "goodbye"





