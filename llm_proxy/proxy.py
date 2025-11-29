from aiohttp import web
import os, json
async def chat(req):
    body = await req.json(); return web.json_response({'result': '{"action":"noop","params":{}}'})
app = web.Application(); app.router.add_post('/chat', chat)
if __name__=='__main__': web.run_app(app, port=int(os.getenv('PORT','11434')))
