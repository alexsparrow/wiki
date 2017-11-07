import datetime

class WikiBackend:
  async def documents(self):
    "List all documents"
    pass

  async def revisions(self, title):
    "Return list of revisions to document as a list"
    pass

  async def document_at(self, title, revision):
    "Return document text at revision"
    pass

  async def add(self, title, text):
    "Create a revision of a document"
    pass
