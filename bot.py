import os
import random
import re
import sqlite3
import telebot
from telebot import types

# ====== НАСТРОЙКИ ======
TOKEN = 8810166498:AAGJOQfxRHeDObU6YtSsjFBw64rTduISOUQ
WORDS_TO_LEARN = 2
DB_FILE = "bot.db"

bot = telebot.TeleBot(TOKEN)

# ====== ГОТОВЫЕ СЛОВА ======
BASE_WORDS = [
    ("кошка", "cat", "🐱"), ("собака", "dog", "🐶"), ("птица", "bird", "🐦"),
    ("рыба", "fish", "🐟"), ("лошадь", "horse", "🐴"), ("корова", "cow", "🐮"),
    ("свинья", "pig", "🐷"), ("овца", "sheep", "🐑"), ("курица", "chicken", "🐔"),
    ("утка", "duck", "🦆"), ("заяц", "rabbit", "🐰"), ("мышь", "mouse", "🐭"),
    ("медведь", "bear", "🐻"), ("лиса", "fox", "🦊"), ("волк", "wolf", "🐺"),
    ("лев", "lion", "🦁"), ("тигр", "tiger", "🐯"), ("слон", "elephant", "🐘"),
    ("обезьяна", "monkey", "🐵"), ("жираф", "giraffe", "🦒"), ("лягушка", "frog", "🐸"),
    ("бабочка", "butterfly", "🦋"), ("пчела", "bee", "🐝"), ("змея", "snake", "🐍"),
    ("черепаха", "turtle", "🐢"), ("пингвин", "penguin", "🐧"), ("сова", "owl", "🦉"),
    ("зебра", "zebra", "🦓"), ("дельфин", "dolphin", "🐬"),
    ("яблоко", "apple", "🍎"), ("банан", "banana", "🍌"), ("апельсин", "orange", "🍊"),
    ("виноград", "grapes", "🍇"), ("арбуз", "watermelon", "🍉"), ("клубника", "strawberry", "🍓"),
    ("лимон", "lemon", "🍋"), ("груша", "pear", "🍐"), ("персик", "peach", "🍑"),
    ("морковь", "carrot", "🥕"), ("помидор", "tomato", "🍅"), ("картошка", "potato", "🥔"),
    ("кукуруза", "corn", "🌽"), ("хлеб", "bread", "🍞"), ("сыр", "cheese", "🧀"),
    ("яйцо", "egg", "🥚"), ("молоко", "milk", "🥛"), ("вода", "water", "💧"),
    ("сок", "juice", "🧃"), ("торт", "cake", "🎂"), ("мороженое", "ice cream", "🍦"),
    ("печенье", "cookie", "🍪"), ("шоколад", "chocolate", "🍫"), ("пицца", "pizza", "🍕"),
    ("суп", "soup", "🍲"), ("мёд", "honey", "🍯"), ("конфета", "candy", "🍬"),
    ("красный", "red", "🔴"), ("синий", "blue", "🔵"), ("зелёный", "green", "🟢"),
    ("жёлтый", "yellow", "🟡"), ("чёрный", "black", "⚫"), ("белый", "white", "⚪"),
    ("фиолетовый", "purple", "🟣"), ("коричневый", "brown", "🟤"), ("розовый", "pink", "💗"),
    ("один", "one", "1️⃣"), ("два", "two", "2️⃣"), ("три", "three", "3️⃣"),
    ("четыре", "four", "4️⃣"), ("пять", "five", "5️⃣"), ("шесть", "six", "6️⃣"),
    ("семь", "seven", "7️⃣"), ("восемь", "eight", "8️⃣"), ("девять", "nine", "9️⃣"),
    ("десять", "ten", "🔟"),
    ("мама", "mom", "👩"), ("папа", "dad", "👨"), ("бабушка", "grandma", "👵"),
    ("дедушка", "grandpa", "👴"), ("брат", "brother", "👦"), ("сестра", "sister", "👧"),
    ("малыш", "baby", "👶"), ("друг", "friend", "🤝"), ("учитель", "teacher", "🧑‍🏫"),
    ("рука", "hand", "✋"), ("нога", "foot", "🦶"), ("глаз", "eye", "👁️"),
    ("нос", "nose", "👃"), ("ухо", "ear", "👂"), ("рот", "mouth", "👄"),
    ("зуб", "tooth", "🦷"), ("сердце", "heart", "❤️"),
    ("дом", "house", "🏠"), ("книга", "book", "📖"), ("стул", "chair", "🪑"),
    ("кровать", "bed", "🛏️"), ("дверь", "door", "🚪"), ("окно", "window", "🪟"),
    ("часы", "clock", "⏰"), ("ключ", "key", "🔑"), ("телефон", "phone", "📱"),
    ("лампа", "lamp", "💡"), ("ручка", "pen", "🖊️"), ("карандаш", "pencil", "✏️"),
    ("мяч", "ball", "⚽"), ("игрушка", "toy", "🧸"), ("зонтик", "umbrella", "☂️"),
    ("сумка", "bag", "👜"), ("шляпа", "hat", "🎩"), ("кроссовки", "shoes", "👟"),
    ("очки", "glasses", "👓"), ("футболка", "t-shirt", "👕"), ("платье", "dress", "👗"),
    ("школа", "school", "🏫"),
    ("солнце", "sun", "☀️"), ("луна", "moon", "🌙"), ("звезда", "star", "⭐"),
    ("облако", "cloud", "☁️"), ("дождь", "rain", "🌧️"), ("снег", "snow", "❄️"),
    ("цветок", "flower", "🌸"), ("дерево", "tree", "🌳"), ("море", "sea", "🌊"),
    ("гора", "mountain", "⛰️"), ("огонь", "fire", "🔥"), ("радуга", "rainbow", "🌈"),
    ("машина", "car", "🚗"), ("автобус", "bus", "🚌"), ("поезд", "train", "🚆"),
    ("самолёт", "plane", "✈️"), ("корабль", "ship", "🚢"), ("велосипед", "bike", "🚲"),
    ("привет", "hello", "👋"), ("пока", "goodbye", "🖐️"), ("спасибо", "thank you", "🙏"),
    ("да", "yes", "✅"), ("нет", "no", "❌"), ("пожалуйста", "please", "🤲"),
]

def icon(e):
    return e or "📝"

# ====== КНОПКИ МЕНЮ ======
BTN_LEARN = "🎯 Учить слова"
BTN_STATS = "📊 Статистика"
BTN_DICT = "📖 Мой словарь"
BTN_ADD = "➕ Добавить слово"
MENU_BUTTONS = [BTN_LEARN, BTN_STATS, BTN_DICT, BTN_ADD]

def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(BTN_LEARN, BTN_STATS)
    kb.row(BTN_DICT, BTN_ADD)
    return kb

# ====== БАЗА ДАННЫХ ======
def db_query(sql, params=(), fetch=False):
    conn = sqlite3.connect(DB_FILE)
    try:
        cur = conn.execute(sql, params)
        result = cur.fetchall() if fetch else None
        conn.commit()
        return result
    finally:
        conn.close()

def init_db():
    db_query("""CREATE TABLE IF NOT EXISTS words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    ru TEXT NOT NULL,
                    en TEXT NOT NULL,
                    emoji TEXT DEFAULT '')""")
    db_query("""CREATE TABLE IF NOT EXISTS progress (
                    user_id INTEGER,
                    word_id INTEGER,
                    correct_count INTEGER DEFAULT 0,
                    PRIMARY KEY (user_id, word_id))""")
    cols = [c[1] for c in db_query("PRAGMA table_info(words)", fetch=True)]
    if "emoji" not in cols:
        db_query("ALTER TABLE words ADD COLUMN emoji TEXT DEFAULT ''")
    for ru, en, emoji in BASE_WORDS:
        exists = db_query("SELECT id FROM words WHERE user_id IS NULL AND ru = ? AND en = ?",
                          (ru, en), fetch=True)
        if exists:
            db_query("UPDATE words SET emoji = ? WHERE id = ?", (emoji, exists[0][0]))
        else:
            db_query("INSERT INTO words (user_id, ru, en, emoji) VALUES (NULL, ?, ?, ?)",
                     (ru, en, emoji))

# ====== ИЗУЧЕНИЕ СЛОВ ======
def send_question(chat_id, user_id):
    rows = db_query(
        """SELECT w.id, w.ru, w.en, w.emoji FROM words w
           LEFT JOIN progress p ON p.word_id = w.id AND p.user_id = ?
           WHERE (w.user_id IS NULL OR w.user_id = ?)
             AND COALESCE(p.correct_count, 0) < ?""",
        (user_id, user_id, WORDS_TO_LEARN), fetch=True)
    if not rows:
        bot.send_message(chat_id,
                         "🎉 Ты выучил все слова! Добавь новые через кнопку «➕ Добавить слово».",
                         reply_markup=main_menu())
        return
    word_id, ru, en, emoji = random.choice(rows)
    all_words = db_query("SELECT id, en FROM words WHERE user_id IS NULL OR user_id = ?",
                         (user_id,), fetch=True)
    others = [w for w in all_words if w[0] != word_id and w[1].lower() != en.lower()]
    wrong = random.sample(others, min(3, len(others)))
    options = wrong + [(word_id, en)]
    random.shuffle(options)
    kb = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=o_en, callback_data=f"ans:{word_id}:{o_id}")
               for o_id, o_en in options]
    kb.add(*buttons)
    bot.send_message(chat_id, f"{icon(emoji)} Как по-английски «{ru}»?", reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data.startswith("ans:"))
def on_answer(call):
    _, word_id, chosen_id = call.data.split(":")
    word_id, chosen_id = int(word_id), int(chosen_id)
    user_id = call.from_user.id
    word = db_query("SELECT ru, en, emoji FROM words WHERE id = ?", (word_id,), fetch=True)[0]
    ru, en, emoji = word
    if word_id == chosen_id:
        db_query("""INSERT INTO progress (user_id, word_id, correct_count) VALUES (?, ?, 1)
                    ON CONFLICT(user_id, word_id)
                    DO UPDATE SET correct_count = correct_count + 1""",
                 (user_id, word_id))
        text = f"✅ Правильно! {icon(emoji)} {ru} — {en}"
    else:
        text = f"❌ Не угадал. Правильно: {icon(emoji)} {ru} — {en}"
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(call.id)
    send_question(call.message.chat.id, user_id)

# ====== СТАТИСТИКА ======
def show_stats(chat_id, user_id):
    learned = db_query(
        """SELECT COUNT(*) FROM progress p JOIN words w ON w.id = p.word_id
           WHERE p.user_id = ? AND p.correct_count >= ?""",
        (user_id, WORDS_TO_LEARN), fetch=True)[0][0]
    total = db_query("SELECT COUNT(*) FROM words WHERE user_id IS NULL OR user_id = ?",
                     (user_id,), fetch=True)[0][0]
    own = db_query("SELECT COUNT(*) FROM words WHERE user_id = ?", (user_id,), fetch=True)[0][0]
    filled = round(10 * learned / total) if total else 0
    bar = "🟩" * filled + "⬜" * (10 - filled)
    bot.send_message(chat_id,
                     f"📊 Твоя статистика\n\n"
                     f"Выучено слов: {learned} из {total}\n{bar}\n"
                     f"Добавлено своих слов: {own}",
                     reply_markup=main_menu())

# ====== СЛОВАРЬ ======
def show_dictionary(chat_id, user_id):
    learned = db_query(
        """SELECT w.ru, w.en, w.emoji FROM progress p JOIN words w ON w.id = p.word_id
           WHERE p.user_id = ? AND p.correct_count >= ? ORDER BY w.ru""",
        (user_id, WORDS_TO_LEARN), fetch=True)
    own = db_query("SELECT ru, en, emoji FROM words WHERE user_id = ? ORDER BY ru",
                   (user_id,), fetch=True)
    text = "📖 Твой словарь\n\n✅ Выученные слова:\n"
    text += "\n".join(f"{icon(e)} {ru} — {en}" for ru, en, e in learned) if learned else "Пока пусто, начни учить слова!"
    text += "\n\n✏️ Мои добавленные слова:\n"
    text += "\n".join(f"{icon(e)} {ru} — {en}" for ru, en, e in own) if own else "Ты пока не добавил свои слова."
    bot.send_message(chat_id, text, reply_markup=main_menu())

# ====== ДОБАВЛЕНИЕ СВОИХ СЛОВ ======
def ask_new_word(chat_id):
    msg = bot.send_message(chat_id,
                           "Напиши слово и перевод через дефис, например:\nяблоко - apple")
    bot.register_next_step_handler(msg, save_new_word)

def save_new_word(message):
    text = (message.text or "").strip()
    if text in MENU_BUTTONS or text.startswith("/"):
        handle_text(message)
        return
    parts = re.split(r"\s*[-—–:]\s*", text, maxsplit=1)
    if len(parts) != 2 or not parts[0] or not parts[1]:
        msg = bot.send_message(message.chat.id, "Не получилось 😕 Напиши так: яблоко - apple")
        bot.register_next_step_handler(msg, save_new_word)
        return
    a, b = parts[0].strip(), parts[1].strip()
    has_ru = lambda s: re.search(r"[а-яёА-ЯЁ]", s) is not None
    has_en = lambda s: re.search(r"[a-zA-Z]", s) is not None
    if has_ru(a) and has_en(b):
        ru, en = a, b
    elif has_ru(b) and has_en(a):
        ru, en = b, a
    else:
        msg = bot.send_message(message.chat.id,
                               "Нужно одно слово по-русски и одно по-английски. Попробуй ещё раз:")
        bot.register_next_step_handler(msg, save_new_word)
        return
    db_query("INSERT INTO words (user_id, ru, en) VALUES (?, ?, ?)",
             (message.from_user.id, ru.lower(), en.lower()))
    bot.send_message(message.chat.id, f"✅ Добавлено: {ru} — {en}", reply_markup=main_menu())

# ====== КОМАНДЫ И МЕНЮ ======
@bot.message_handler(commands=["start", "help"])
def start(message):
    bot.send_message(message.chat.id,
                     "Привет! 👋 Я помогу выучить английские слова.\n"
                     "Выбери, что хочешь сделать:",
                     reply_markup=main_menu())

@bot.message_handler(content_types=["text"])
def handle_text(message):
    chat_id, user_id, text = message.chat.id, message.from_user.id, message.text
    if text == BTN_LEARN:
        send_question(chat_id, user_id)
    elif text == BTN_STATS:
        show_stats(chat_id, user_id)
    elif text == BTN_DICT:
        show_dictionary(chat_id, user_id)
    elif text == BTN_ADD:
        ask_new_word(chat_id)
    else:
        bot.send_message(chat_id, "Выбери кнопку в меню 👇", reply_markup=main_menu())

# ====== ЗАПУСК ======
if __name__ == "__main__":
    init_db()
    print("Бот запущен!")
    bot.infinity_polling()
