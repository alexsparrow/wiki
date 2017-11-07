import datetime

from .backend import WikiBackend

class InMemoryBackend(WikiBackend):
  """
  This is just a basic in-memory backend I used for some of the tests.
  """
  def __init__(self, data):
    self._data = data

  async def documents(self):
    return list(self._data.keys())

  async def revisions(self, title):
    if not title in self._data:
      return None
    return [timestamp.timestamp() for timestamp, _ in self._data[title]]

  async def document_at(self, title, revision):
    if not title in self._data:
      return None
    documents = [doc for rev, doc in self._data[title] if rev.timestamp() == revision]

    if not documents:
      return None

    return documents[0]

  async def add(self, title, text):
    timestamp = datetime.datetime.now()
    self._data.setdefault(title, []).append((timestamp, text))
    return timestamp.timestamp()

