import os
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = os.getenv("BOT_TOKEN")


# ======= ТВОИ ТАБЛИЦЫ =======

merchants_table = {
    (1, 6): "Алкоголь и напитки",
    (7, 10): "Животные (ездовые и домашние)",
    (11, 15): "Книги и карты (обычные)",
    (16, 19): "Цветы и семена",
    (20, 25): "Еда и части животных",
    (25, 29): "Мебель и предметы интерьера",
    (30, 34): "Высокая мода",
    (35, 38): "Ювелирные изделия",
    (39, 43): "Безделушки",
    (44, 48): "Изделия из кожи",
    (49, 52): "Механические приспособления",
    (53, 57): "Средние и тяжелые доспехи (щиты)",
    (58, 61): "Зелья, яды и травы",
    (62, 66): "Религиозные товары",
    (67, 71): "Песни и инструменты",
    (72, 75): "Книги заклинаний и свитки",
    (76, 80): "Воровские приспособления",
    (81, 86): "Инструменты",
    (87, 91): "Транспортные средства и перевозки",
    (92, 96): "Оружие",
    (97, 100): "Легендарный торговец"
}

legendary_table = {
    1: "Астральный путешественник",
    2: "Чары",
    3: "Чары",
    4: "Предложения фей",
    5: "Магические предметы",
    6: "Магические предметы",
    7: "Волшебные существа",
    8: "Волшебные существа",
    9: "Некромантия",
    10: "Некромантия",
    11: "Необходимые вещи",
    12: "Затерявшиеся во времени"
}

qualification_table = {
    (1, 1): ("Ужасная", 20),
    (2, 4): ("Плохая", 50),
    (5, 7): ("Средняя", 100),
    (8, 10): ("Хорошая", 250),
    (11, 12): ("Прекрасная", 500)
}


# ======= ЛОГИКА =======

def get_category(roll):
    for (start, end), category in merchants_table.items():
        if start <= roll <= end:
            return category
    return "Неизвестно"


def get_qualification(roll, is_legendary):
    if is_legendary and roll <= 4:
        roll = 5
    for (start, end), (level, money_base) in qualification_table.items():
        if start <= roll <= end:
            return level, 10 * money_base
    return "Неизвестно", 0


def generate_merchants(num_merchants):
    results = []
    for _ in range(num_merchants):
        roll100 = random.randint(1, 100)
        is_legendary = (97 <= roll100 <= 100)

        if is_legendary:
            roll12 = random.randint(1, 12)
            category = legendary_table[roll12]
        else:
            category = get_category(roll100)

        qual_roll = random.randint(1, 12)
        qual_level, _ = get_qualification(qual_roll, is_legendary)

        results.append({
            "Категория": category,
            "Квалификация": qual_level,
            "Легендарный": is_legendary
        })
    return results


def format_merchants(num):
    merchants = generate_merchants(num)

    lines = ["🎲 Сгенерированные торговцы:", "—" * 40]

    for i, m in enumerate(merchants, 1):
        cat = m["Категория"]
        if m["Легендарный"]:
            cat += " (Л)"

        lines.append(f"{i:2}. {cat} | {m['Квалификация']}")

    lines.append("—" * 40)

    return "\n".join(lines)


# ======= ОБРАБОТЧИКИ БОТА =======

def start(update, context):
    update.message.reply_text(
        "Привет! Я генерирую торговцев для D&D 🎲\n\n"
        "Используй команду:\n"
        "/gen 10 — чтобы сгенерировать 10 торговцев"
    )


def gen(update, context):
    try:
        if context.args:
            num = int(context.args[0])
        else:
            num = 10
    except:
        num = 10

    if num < 1:
        num = 1
    if num > 50:
        num = 50

    text = format_merchants(num)
    update.message.reply_text(text)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("gen", gen))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":

    main()
