import asyncio
import datetime

from aiohttp import web
from .filesystem import FileSystemBackend

def create_web_app(backend):
  async def documents(request):
    documents = await backend.documents()
    return web.json_response(documents)

  async def revisions(request):
    revisions = await backend.revisions(request.match_info["title"])
    if revisions:
      return web.json_response(revisions)
    else:
      return web.HTTPNotFound()

  async def document_at(request):
    title = request.match_info["title"]
    timestamp = int(request.match_info["timestamp"])
    revisions = await backend.revisions(title)

    if revisions:
      revisions.sort(key=lambda rev: rev)
      revisions_pre_timestamp = [rev for rev in revisions if rev < timestamp]

      if revisions_pre_timestamp:
        doc = await backend.document_at(title, revisions_pre_timestamp[-1])
        return web.json_response(doc)

    return web.HTTPNotFound()

  async def document_latest(request):
    title = request.match_info["title"]
    revisions = await backend.revisions(title)

    if revisions:
      doc = await backend.document_at(title, revisions[-1])
      return web.json_response(doc)

    return web.HTTPNotFound()

  async def document_add(request):
    title = request.match_info["title"]
    data = await request.json()

    revision = await backend.add(title, data)

    return web.json_response(revision)

  app = web.Application()
  app.router.add_get('/documents', documents)
  app.router.add_get('/documents/{title}', revisions)
  app.router.add_get('/documents/{title}/latest', document_latest)
  app.router.add_get('/documents/{title}/{timestamp}', document_at)
  app.router.add_post('/documents/{title}', document_add)
  return app

if __name__ == "__main__":
  loop = asyncio.get_event_loop()
  backend = FileSystemBackend("data", loop)
  app = create_web_app(backend)
  web.run_app(app)
