try:
    from PIL import Image
except ImportError:
    import Image
from PIL import ImageEnhance, ImageFilter
from pytesseract import image_to_string, image_to_boxes
import json, os, re, urllib.request
from dotenv import load_dotenv
from telebot import TeleBot


def ExportURL(image):
    im = Image.open(image)
    im = im.filter(ImageFilter.MedianFilter())
    enhance = ImageEnhance.Contrast(im)
    im = enhance.enhance(2)
    im.convert("1")
    t = image_to_string(im)
    url = re.findall("(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+", t)
    return "\n".join(url) if len(url) > 0 else "there no links"


load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]
bot = TeleBot(BOT_TOKEN)


@bot.message_handler(content_types=["photo"])
def get_url(message):
    json_text = str(bot.get_file(message.photo[-1].file_id)).replace("'", '"')
    img_path = json.loads(json_text)["file_path"]
    img_name = img_path.split("/")[1]
    img_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{img_path}"
    urllib.request.urlretrieve(img_url, img_name)
    contnet = ExportURL(img_name)
    os.remove(img_name)
    bot.send_message(message.chat.id, contnet)

bot.polling()
