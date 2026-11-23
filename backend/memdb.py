"""Database lokal ringan (tanpa MongoDB) yang meniru subset API pymongo.

Dipakai untuk tes (path=None, murni di memori) dan untuk mode ``DB_MODE=local``
(path=file JSON, data tetap ada setelah server di-restart). Cocok untuk
pengembangan/demo skala kecil, bukan untuk produksi.
"""

from __future__ import annotations

import copy
import json
import os
import threading
from datetime import datetime


def _match(doc, query):
    for k, v in query.items():
        val = doc.get(k)
        if isinstance(v, dict) and "$in" in v:
            if val not in v["$in"]:
                return False
        elif val != v:
            return False
    return True


class Cursor:
    def __init__(self, docs):
        self.docs = docs

    def sort(self, key, direction=1):
        if isinstance(key, list):
            key, direction = key[0]
        self.docs.sort(key=lambda d: d.get(key), reverse=direction == -1)
        return self

    def limit(self, n):
        self.docs = self.docs[:n]
        return self

    def __iter__(self):
        return iter(self.docs)


class Collection:
    def __init__(self, on_change=None):
        self.docs = []
        self._on_change = on_change or (lambda: None)

    def create_index(self, *a, **kw):
        pass

    def insert_one(self, doc):
        self.docs.append(copy.deepcopy(doc))
        self._on_change()

    def find_one(self, query=None):
        for d in self.docs:
            if _match(d, query or {}):
                return copy.deepcopy(d)
        return None

    def find(self, query=None):
        return Cursor([copy.deepcopy(d) for d in self.docs if _match(d, query or {})])

    def update_one(self, query, update, upsert=False):
        for d in self.docs:
            if _match(d, query):
                d.update(copy.deepcopy(update.get("$set", {})))
                self._on_change()
                return
        if upsert:
            d = {**query, **update.get("$setOnInsert", {}), **update.get("$set", {})}
            self.docs.append(copy.deepcopy(d))
            self._on_change()

    def delete_one(self, query):
        for i, d in enumerate(self.docs):
            if _match(d, query):
                del self.docs[i]
                self._on_change()
                return

    def delete_many(self, query):
        self.docs = [d for d in self.docs if not _match(d, query)]
        self._on_change()

    def count_documents(self, query):
        return sum(1 for d in self.docs if _match(d, query))


def _enc(o):
    if isinstance(o, datetime):
        return {"$date": o.isoformat()}
    raise TypeError(f"tidak bisa disimpan: {type(o)}")


def _dec(d):
    return datetime.fromisoformat(d["$date"]) if set(d) == {"$date"} else d


class LocalDB:
    """Akses koleksi lewat atribut: ``db.users``, ``db.documents``, dst."""

    def __init__(self, path: str | None = None):
        self._path = path
        self._lock = threading.RLock()
        self._c: dict[str, Collection] = {}
        if path and os.path.isfile(path):
            with open(path, encoding="utf-8") as fh:
                raw = json.load(fh, object_hook=_dec)
            for name, docs in raw.items():
                self._coll(name).docs = docs

    def _coll(self, name):
        if name not in self._c:
            self._c[name] = Collection(self._save)
        return self._c[name]

    def _save(self):
        if not self._path:
            return
        with self._lock:
            os.makedirs(os.path.dirname(self._path) or ".", exist_ok=True)
            tmp = self._path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as fh:
                json.dump({n: c.docs for n, c in self._c.items()}, fh, default=_enc, ensure_ascii=False)
            os.replace(tmp, self._path)

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        return self._coll(name)


FakeDB = LocalDB  # alias untuk tes
