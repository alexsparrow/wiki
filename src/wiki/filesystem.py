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

  async def _path_exists(self, path):
    # This is IO so in principle I think it can block :-(
    return await self._run_blocking(lambda: os.path.exists(path))

  async def _run_blocking(self, func):
    return await self._loop.run_in_executor(None, func)

  async def documents(self):
    return await self._run_blocking(lambda: os.listdir(self._path))

  async def revisions(self, title):
    path = self._document_path(title)
    if not await self._path_exists(path):
      return None
    return await self._run_blocking(lambda: [rev for rev in os.listdir(path)])

  async def document_at(self, title, revision):
    path = self._revision_path(title, revision)

    if not await self._path_exists(path):
      return None

    return await self._run_blocking(lambda: open(path).read())

  async def add(self, title, text):
    timestamp = datetime.datetime.now().timestamp()

    document_path = self._document_path(title)

    def _make_dirs():
      if not os.path.exists(document_path):
        os.makedirs(document_path)

    await self._run_blocking(_make_dirs)

    revision_path = self._revision_path(title, timestamp)
    await self._run_blocking(lambda: open(revision_path, "w").write(text))

    return timestamp
