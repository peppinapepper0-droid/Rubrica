import asyncio
import tornado.web
import tornado.escape

from backend.db import COOKIE_SECRET, PORT
from backend.handlers.mail_psw import RegisterHandler, LoginHandler, LogoutHandler
from backend.handlers.messaggi import TasksHandler,  TaskDeleteHandler


def make_app():
    return tornado.web.Application(
        [
            (r"/api/register", RegisterHandler),  # per registrazione
            (r"/api/login", LoginHandler),  # per login (accesso)
            (r"/api/logout", LogoutHandler),  # per logout

            (r"/api/tasks", TasksHandler),  # avere/creare nuovo messaggio
            (r"/api/tasks/([a-f0-9]{24})/delete", TaskDeleteHandler),  # eliminare msg in base a ID

            (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),

            (r"/", tornado.web.RedirectHandler, {"url": "/static/login.html"}),
            # quando url è "/", utente viene reinderizzato alla pagina di login
        ],
        cookie_secret=COOKIE_SECRET,
        autoreload=True,
        debug=True
    )


async def main():
    app = make_app()
    app.listen(PORT)
    print(f"Server avviato su http://localhost:{PORT}")

    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer spento.")
    except Exception as e:
        print(f"Errore critico durante l'avvio del server: {e}")
