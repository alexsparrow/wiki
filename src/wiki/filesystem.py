import os
import os.path
import concurrent.futures
import datetime

from .backend import WikiBackend

class FileSystemBackend(WikiBackend):
  def __init__(self, path, loop):
    if not os.path.exists(path):
      os.makedirs(path)
    self._path = path
    self._loop = loop

  def _document_path(self, title):
    return os.path.join(self._path, title)

  def _revision_path(self, title, revision):
    return os.path.join(self._path, title, str(revision))

  async def documents(self):
    return await self._loop.run_in_executor(None, lambda: os.listdir(self._path))

  async def revisions(self, title):
    path = self._document_path(title)
    if not os.path.exists(path):
      return None
    return await self._loop.run_in_executor(None, lambda: [rev for rev in os.listdir(path)])

  async def document_at(self, title, revision):
    path = self._revision_path(title, revision)

    if not os.path.exists(path):
      return None

    return await self._loop.run_in_executor(None, lambda: open(path).read())

  async def add(self, title, text):
    timestamp = datetime.datetime.now().timestamp()

    document_path = self._document_path(title)
    if not os.path.exists(document_path):
      os.makedirs(document_path)

    revision_path = self._revision_path(title, timestamp)
    await self._loop.run_in_executor(None, lambda: open(revision_path, "w").write(text))

    return timestamp
