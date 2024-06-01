from flask import Flask
from enma import Enma
from tinydb import TinyDB

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

enma = Enma()
db =  TinyDB("cache.json")

enma.source_manager.set_source("manganato")

MANGA_LIST = ["manga-fh982764", "manga-wh999390", "manga-um972295", "manga-wf999788", "manga-pn992622", "manga-je986761", "manga-ts997253", "manga-pd992912"]

@app.route("/")
def home():
  return "hello world"

@app.route("/get_updates")
def get_updates():
  
  def get_cache():
    return db.all()
  
  def fetch_manga(id):
    manga = enma.get(identifier=id)
    return { "title": manga.title.english, "chapters": len(manga.chapters) }

  cached_mangas = get_cache();
  mangas = list(map(fetch_manga, MANGA_LIST))
  manga_with_new_chapters = []

  for manga1, manga2 in zip(cached_mangas, mangas):
    if manga1["chapters"] != manga2["chapters"]:
      manga_with_new_chapters.append(manga2["title"])

  new_chapters_count = len(manga_with_new_chapters)

  db.truncate()
  for manga in mangas: 
    db.insert(manga)
  
  return { "count" : new_chapters_count, "names": manga_with_new_chapters }

if __name__ == "__main__":
  app.run()