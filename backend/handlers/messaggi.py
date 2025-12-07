import tornado.escape
from bson import ObjectId
from backend.db import messaggi
from backend.handlers.mail_psw import BaseHandler
import datetime


class TasksHandler(BaseHandler):
    async def get(self):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)

        cursor = messaggi.find({"user_id": ObjectId(user["id"])})
        bacheca = []
        async for messaggio in cursor:
            bacheca.append({
                "id": str(messaggio["_id"]),
                "autore": messaggio["autore"],
                "text": messaggio["text"],
                "data": messaggio["data"],
                "done": messaggio["done"],
                "cestino": str(messaggio["user_id"])
            })

        return self.write_json({"creatore":user["id"],"items": bacheca})

    async def post(self):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)

        body = tornado.escape.json_decode(self.request.body)
        text = body.get("text", "").strip()

        if not text:
            return self.write_json({"error": "Testo obbligatorio"}, 400)

        result = await messaggi.insert_one({
            "user_id": ObjectId(user["id"]),
            "text": text,
            "autore": autore,
            "data":datetime.datetime.now()
        })

        return self.write_json({"id": str(result.inserted_id)}, 201)


class TaskUpdateHandler(BaseHandler):
    async def put(self, task_id):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)

        body = tornado.escape.json_decode(self.request.body)
        done = body.get("done")

        await messaggi.update_one(
            {"_id": ObjectId(task_id), "user_id": ObjectId(user["id"])},
            {"$set": {"done": bool(done)}}
        )

        return self.write_json({"message": "Aggiornato"})


class TaskDeleteHandler(BaseHandler):
    async def delete(self, task_id):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)

        await messaggi.delete_one({
            "_id": ObjectId(task_id),
            "user_id": ObjectId(user["id"])
        })

        return self.write_json({"message": "Eliminato"})
