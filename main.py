import logging, os, re
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

from dotenv import load_dotenv


load_dotenv()

#Fucntion
def get_random_string(length):
    import random, string
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def convert_round(file):
    import subprocess
    try:
        subprocess.run([
            'ffmpeg','-hide_banner', '-loglevel', 'error', '-i', file, '-r', '30', '-t', '2.99', 
            '-filter_complex', "[0:v]scale=512:512:force_original_aspect_ratio=decrease,crop=ih:ih[video square];[video square]split=3[black canvas][white canvas][video square];[black canvas]setsar=1:1,drawbox=color=black@1:t=fill[black background];[white canvas]scale=w=iw:h=iw,format=yuva444p,geq=lum='p(X,Y)':a='st(1,pow((W-10),2)/4)+st(3,pow(X-(W/2),2)+pow(Y-(H/2),2));if(lte(ld(3),ld(1)),255,0)',drawbox=color=white@1:t=fill[scaled up white circle];[scaled up white circle]scale=w=iw:h=iw[white circle];[black background][white circle]overlay[alpha mask];[video square][alpha mask]alphamerge,format=yuva420p",
            '-filter_complex_threads', '1', '-c:v', 'libvpx-vp9', '-auto-alt-ref', '0', '-preset', 'ultrafast', '-an', '-b:v', '400K', file.replace(".mp4", ".webm")])
        os.remove(file)
        return True
    except Exception as e:
        os.remove(file)
        logging.warning('Error at %s', 'division', exc_info=e)
        return False

def convert_video(file):
    import subprocess
    try:
        subprocess.run([
            'ffmpeg','-hide_banner', '-loglevel', 'error', '-y', '-i', file, '-r', '30', '-t', '2.99',           
             '-an', '-c:v', 'libvpx-vp9','-pix_fmt', 'yuva420p' , '-vf', 'scale=512:512:force_original_aspect_ratio=decrease', '-b:v', '400K', file.replace(".mp4", ".webm")])
        os.remove(file)
        return True
    except Exception as e:
        os.remove(file)
        logging.warning('Error at %s', 'division', exc_info=e)
        return False

def resize_image(file, size=(512, 512)):
    from PIL import Image 
    try:
        original_image = Image.open(file)
        width, height = original_image.size
        rel = max(width, height) / 512
        width = int(width / rel) 
        height = int(height / rel)
        size = (width, height)
        resized_image = original_image.resize(size)
        resized_image.save(file)
    except Exception as e:
        os.remove(file)
        logging.warning('Error at %s', 'division', exc_info=e)

#Startup
logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.getenv("TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
# States
class Form(StatesGroup):
    name = State()
    media_add = State()
    title_pack = State()
    name_pack = State()
    photo = State()
    convert_round = State()
    convert_vid = State()
    #title_videopack = State()
    #name_videopack = State()
    #video = State()

#Cancel
@dp.message_handler(state='*', commands='cancel')
async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Скасовано(', reply_markup=types.ReplyKeyboardRemove())

#Complete
@dp.message_handler(state='*', commands='complete')
async def start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if(data['name'] is None):
            return
        try:
            StickerSet = await bot.get_sticker_set(data['name'])
        except:
            return
        await message.answer(f"<a href = \"https://t.me/addstickers/{StickerSet.name}\">{StickerSet.title}</a> додано нові наліпки🥰", parse_mode='HTML')
        await state.finish()


# Start
@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer("Привіт! \nЯ маленький український бот, що допомогає користувачам створювати свої наліпки) \nСподіваюсь, Вам сподобається!)\n/newpack – Створюю новий пак наліпок\n/addsticker - Додаю наліпку до існуючого паку\n/convertround - конвертування \"кружечків\"\n/convertvideo - Конвертування відео\n/cancel - Скасувати дію")

#addSticker
@dp.message_handler(commands='addsticker')
async def addSticker(message: types.Message):
    await Form.name.set()
    me = await bot.get_me()
    await message.reply(f"Спочатку, будь ласка, введи назву існуючого паку наліпок(необхідно, щоб він закінчувався на \"_by_{me.username}\"))")

#inputStickerPack
@dp.message_handler(state=Form.name)
async def inputStickerPack(message: types.Message, state: FSMContext):
    myinfo = await bot.get_me()
    txtmsg = message.text
    if(not f"_by_{myinfo.username}" in txtmsg):
        txtmsg += f"_by_{myinfo.username}"
    try:
        StickerSet = await bot.get_sticker_set(txtmsg)
        if(len(StickerSet.stickers) >= 120):
            return await message.reply("Нажаль, кількість наліпок досягла максимуму((\n\nУ одному паку може бути максимум лише 120 наліпок, тому пропоную створити новий пак за допомогою команди /newpack")
    except:
        return await message.reply("Упс... Не знайшов цього паку наліпок:(\nМожливо Ви допустили помилку, спробуйте ще!")

    async with state.proxy() as data:
        data['name'] = txtmsg
    
    await Form.media_add.set()
    await message.reply(f"Вибран пак <a href = \"https://t.me/addstickers/{StickerSet.name}\">{StickerSet.title}</a>\nВідправте фото щоб додати(по одному)", parse_mode='HTML')

#incorrectPhoto
@dp.message_handler(lambda message: message.content_type!='photo' , state=Form.media_add)
async def incorrectPhoto(message: types.Message):
    return await message.reply("Це, звісно, прекрасно, але будь ласка, відправ фотографію(")

#addStickerToPack
@dp.message_handler(content_types=['photo'], state=Form.media_add)
async def addStickerToPack(message: types.Message, state: FSMContext):
    #photoID
    if(message['media_group_id'] == None):
        photo_id = message['photo'][0]['file_unique_id']
    else:
        photo_id = message['media_group_id']
    #checkGroupPhoto
    async with state.proxy() as data:
        try:
            if(data['media_add'] == photo_id):
                return
        except:
            pass

        data['media_add'] = photo_id
    #downloadPhoto
    await message.photo[-1].download(destination_file="file/"+photo_id +".png")
    #changeResolution
    resize_image("file/"+photo_id +".png")
    #formWorker
    async with state.proxy() as data:
        #checkError
        try:
            #tryToAddSticker
            if( await bot.add_sticker_to_set(
                    user_id = message.from_id, 
                    name = data['name'], 
                    emojis= '❤️',
                    png_sticker= open("file/"+data['media_add']+'.png', 'rb')
                    )):
                await message.reply(f"Додано до паку, ви можете додавати ще... \nЩоб зупинитись, напишіть /complete")
                #deletePhoto
                os.remove("file/"+data['media_add']+'.png')
            else:
                await message.reply(f"Якісь помилки, спробуйте відправити ще раз(")
                os.remove("file/"+data['media_add']+'.png')
        except:
            await message.reply(f"Якісь помилки, спробуйте відправити ще раз(")
            #deletePhoto
            os.remove("file/"+data['media_add']+'.png')
        
#startNewStickerpack
@dp.message_handler(commands='newpack')
async def startNewStickerpack(message: types.Message):
    await Form.title_pack.set()
    await message.reply("Спочатку, будь ласка, введи назву майбутнього паку наліпок)")

#incorrecttitle
@dp.message_handler(lambda message: len(message.text)>30, state=Form.title_pack)
async def incorrecttitle(message: types.Message):
    return await message.reply("Будь ласка, не більше 30 символів у назві, ніхто ж не зрозуміє тоді((\nМоя порада, обмежтесь 10-15 символами")

#addTitle
@dp.message_handler(lambda message: len(message.text)<=30, state=Form.title_pack)
async def addTitle(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title_pack'] = message.text
    await Form.next()
    await message.reply("Дякую🥰 \nТелеграму необхідно щоб ти ввів коротку назву.\n\nЗ оффіційної документації: \n\"Коротка назва набору наклейок для використання в URL-адресах t.me/addstickers/ (наприклад, animals). Може містити лише англійські літери, цифри та підкреслення.\"")

#incorrectName1
@dp.message_handler(lambda message: len(re.sub(r'[^a-zA-Z]', '', message.text[0])) == 0, state=Form.name_pack)
async def incorrectName(message: types.Message):
    return await message.reply("Коротка назва повинна починатися з англійської літери")

#incorrectName
@dp.message_handler(lambda message: len(message.text)>15 or len(re.sub(r'[^a-zA-Z]', '', message.text)) == 0, state=Form.name_pack)
async def incorrectName(message: types.Message):
    return await message.reply("Будь ласка, вводьте не більше 15 символів у короткій назві та використовуйте лише латинські літери, цифри та підкреслення")

#addName
@dp.message_handler(lambda message: len(message.text)<=15 and len(re.sub(r'[^a-zA-Z]', '', message.text[0])) == 1, state=Form.name_pack)
async def addName(message: types.Message, state: FSMContext):
    #formatNameToCorrect
    result = str(message.text)
    #result = re.sub(r'[^a-zA-Z0-9_]', '', result)
    #checkUniqueName
    myinfo = await bot.get_me()
    try:
        StickerSet = await bot.get_sticker_set(result+"_by_"+myinfo.username)
    except:
        StickerSet = None
    if(StickerSet != None):
        return await message.reply("Нажаль з такою назвою вже існує інший пак наліпок(\nСпробуйте іншу назву!")
    #addName
    async with state.proxy() as data:
        data['name_pack'] = result
    await Form.next()
    await message.reply("Дякую❤️\nВідправте фотографію на першу наліпку)")

#incorrectPhoto
@dp.message_handler(lambda message: message.content_type!='photo' , state=Form.photo)
async def incorrectPhoto(message: types.Message):
    return await message.reply("Це, звісно, прекрасно, але будь ласка, відправ фотографію(")

#addPhotoandSend
@dp.message_handler(content_types=['photo'], state=Form.photo)
async def photo_correct(message: types.Message, state: FSMContext):
    #checkGroupPhoto
    if(message['media_group_id'] == None):
        photo_id = message['photo'][0]['file_unique_id']
    else:
        photo_id = message['media_group_id']

    async with state.proxy() as data:
        try:
            if(data['photo'] == photo_id):
                return
        except:
            pass
        data['photo'] = photo_id
    
    #checkUniqueName
    result = str(message.text)
    #result = re.sub(r'[^a-zA-Z0-9_]', '', message.text)
    myinfo = await bot.get_me()
    try:
        StickerSet = await bot.get_sticker_set(result+"_by_"+myinfo.username)
    except:
        StickerSet = None
    if(StickerSet !=None):
        Form.name.set()
        return await message.reply("Нажаль з такою назвою вже існує інший пак наліпок(\nСпробуйте іншу назву!")

    #downloadPhoto
    await message.photo[-1].download(destination_file="file/"+photo_id +".png")
    #changeResolution
    resize_image("file/"+photo_id +".png")
    myinfo = await bot.get_me()
    #formWorker
    async with state.proxy() as data:
        #tryToCreateStickerPack
        if( await bot.create_new_sticker_set(
                user_id = message.from_id, 
                name = data['name_pack'] + "_by_" + myinfo.username, 
                title = data['title_pack'] + " | by @"+myinfo.username,
                emojis= '❤️',
                png_sticker= open("file/"+data['photo']+'.png', 'rb')
                )):
            await message.reply(f"Створено новий пак наліпок t.me/addstickers/{data['name_pack']}_by_{myinfo.username}")
            await state.finish()
            #deletePhoto
            os.remove("file/"+data['photo']+'.png')



#startNewStickerpack
@dp.message_handler(commands='convertround')
async def convertRound(message: types.Message):
    await Form.convert_round.set()
    await message.reply("Відправте відео/gif відеоповідомлення чи прешліть відеоповідомлення у цей чат\nЩоб завершити конвертування натисніть /cancel")

@dp.message_handler(commands='convertvideo')
async def convertVideo(message: types.Message):
    await Form.convert_vid.set()
    await message.reply("Відправте відео у цей чат\nЩоб завершити конвертування натисніть /cancel")


@dp.message_handler(content_types=[types.ContentType.VIDEO, types.ContentType.VIDEO_NOTE, types.ContentType.ANIMATION], state=Form.convert_round)
async def videocorrect(message: types.Message, state: FSMContext):
    await bot.send_chat_action(message.from_id, 'upload_document')
    if(message.content_type in [types.ContentType.VIDEO_NOTE]):
        idfile = message.video_note.file_id
    elif(message.content_type in [types.ContentType.VIDEO]):
        idfile = message.video.file_id
    elif(message.content_type in [types.ContentType.ANIMATION]):
        idfile = message.animation.file_id
    file_info = await bot.get_file(idfile)
    try:
            await bot.download_file(file_info.file_path, "file/"+idfile +".mp4")
            if convert_round("file/"+str(idfile) +".mp4"):
                await message.reply_document(open("file/"+str(idfile) +".webm", 'rb'), caption="Щоб закінчити потік конвертування натисніть /cancel")
            else:
                await message.reply("Скоріш за все ви відправили неправильне відео(воно не квадратне), чи проблема з конвертуванням\nСпробуйте /convertvideo для конвертування)")
    except Exception as e:
        logging.warning('Error at %s', 'division', exc_info=e)
    os.remove("file/"+str(idfile) +".webm")

@dp.message_handler(content_types=[types.ContentType.VIDEO, types.ContentType.ANIMATION], state=Form.convert_vid)
async def videocorrect(message: types.Message, state: FSMContext):
    await bot.send_chat_action(message.from_id, 'upload_document')
    if(message.content_type in [types.ContentType.VIDEO]):
        idfile = message.video.file_id
    elif(message.content_type in [types.ContentType.ANIMATION]):
        idfile = message.animation.file_id
    file_info = await bot.get_file(idfile)
    try:
            await bot.download_file(file_info.file_path, "file/"+idfile +".mp4")
            if convert_video("file/"+str(idfile) +".mp4"):
                await message.reply_document(open("file/"+str(idfile) +".webm", 'rb'), caption="Щоб закінчити потік конвертування натисніть /cancel")
            else:
                await message.reply("Проблема з конвертуванням")
    except Exception as e:
        logging.warning('Error at %s', 'division', exc_info=e)
    os.remove("file/"+str(idfile) +".webm")

'''
@dp.message_handler(content_types=types.ContentType.ANY)
async def mdc_all(message: types.Message):
    if(message.content_type in [types.ContentType.VIDEO_NOTE]):
        await bot.send_chat_action(message.from_id, 'upload_document')
        file_info = await bot.get_file(message.video_note.file_id)
        try:
            await bot.download_file(file_info.file_path, "file/"+message.video_note.file_id +".mp4")
            convert_video("file/"+str(message.video_note.file_id) +".mp4")
            await message.reply_document(open("file/"+str(message.video_note.file_id) +".webm", 'rb'))
            os.remove("file/"+str(message.video_note.file_id) +".webm")
        except Exception as e:
            os.remove("file/"+str(message.video_note.file_id) +".webm")
            logging.warning('Error at %s', 'division', exc_info=e)'''


#does not work on Aiogram 2.x, works on 3.x, but needs an upgrade code and it takes a long time
'''
#startNewRoundStickerpack
@dp.message_handler(commands='newvideopack')
async def startNewStickerpackV(message: types.Message):
    await Form.title_videopack.set()
    await message.reply("Спочатку, будь ласка, введи назву майбутнього паку відео-наліпок)")

#incorrecttitle
@dp.message_handler(lambda message: len(message.text)>30, state=Form.title_videopack)
async def incorrecttitle(message: types.Message):
    return await message.reply("Будь ласка, не більше 30 символів у назві, ніхто ж не зрозуміє тоді((\nМоя порада, обмежтесь 10-15 символами")

#addTitle
@dp.message_handler(lambda message: len(message.text)<=30, state=Form.title_videopack)
async def addTitleV(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title_videopack'] = message.text
    await Form.name_videopack.set()
    await message.reply("Дякую🥰 \nТелеграму необхідно щоб ти ввів коротку назву.\n\nЗ оффіційної документації: \n\"Коротка назва набору наклейок для використання в URL-адресах t.me/addstickers/ (наприклад, animals). Може містити лише англійські літери, цифри та підкреслення.")

#incorrectName1
@dp.message_handler(lambda message: len(re.sub(r'[^a-zA-Z]', '', message.text[0])) == 0, state=Form.name_videopack)
async def incorrectNameV1(message: types.Message):
    return await message.reply("Коротка назва повинна починатися з англійської літери")

#incorrectName
@dp.message_handler(lambda message: len(message.text)>15 or len(re.sub(r'[^a-zA-Z]', '', message.text)) == 0, state=Form.name_videopack)
async def incorrectNameV(message: types.Message):
    return await message.reply("Будь ласка, вводьте не більше 15 символів у короткій назві та використовуйте лише латинські літери, цифри та підкреслення")

#addName
@dp.message_handler(lambda message: len(message.text)<=15 and len(re.sub(r'[^a-zA-Z]', '', message.text)) >= 1 and len(re.sub(r'[^a-zA-Z]', '', message.text[0])) > 0, state=Form.name_videopack)
async def addNameV(message: types.Message, state: FSMContext):
    #formatNameToCorrect
    result = str(message.text)
    #result = re.sub(r'[^a-zA-Z0-9_]', '', result)
    #checkUniqueName
    myinfo = await bot.get_me()
    try:
        StickerSet = await bot.get_sticker_set(result+"_by_"+myinfo.username)
    except:
        StickerSet = None
    if(StickerSet != None):
        return await message.reply("Нажаль з такою назвою вже існує інший пак наліпок(\nСпробуйте іншу назву!")
    #addName
    async with state.proxy() as data:
        data['name_videopack'] = result
    await Form.video.set()
    await message.reply("Дякую❤️\nПерешліть у цей чат відеосповіщення на першу наліпку)")

#incorrectPhoto
@dp.message_handler(lambda message: message.content_type!='video_note' , state=Form.video)
async def incorrectPhotoV(message: types.Message):
    return await message.reply("Це, звісно, прекрасно, але будь ласка, відправте відеосповіщення(")

#addPhotoandSend
@dp.message_handler(content_types=['video_note'], state=Form.video)
async def photo_correctV(message: types.Message, state: FSMContext):
    #checkGroupPhoto]
    async with state.proxy() as data:
        data['video'] = message.video_note.file_id
    
    #checkUniqueName
    async with state.proxy() as data:
        result = str(data['name_videopack'])
        #result = re.sub(r'[^a-zA-Z0-9_]', '', message.text)
        myinfo = await bot.get_me()
        try:
            StickerSet = await bot.get_sticker_set(result+"_by_"+myinfo.username)
        except:
            StickerSet = None
        if(StickerSet !=None):
            Form.name_videopack.set()
            return await message.reply("Нажаль з такою назвою вже існує інший пак наліпок(\nСпробуйте іншу назву!")
        #downloadPhoto
        file_info = await bot.get_file(data['video'])
        await bot.download_file(file_info.file_path, "file/"+data['video'] +".mp4")

        #changeResolution
        convert_video("file/"+str(data['video']) +".mp4")
        myinfo = await bot.get_me()
        #formWorker
        #tryToCreateStickerPack
        if( await bot.create_new_sticker_set(
                user_id = message.from_user.id, 
                name = data['name_videopack'] + "_by_" + myinfo.username, 
                title = data['title_videopack'] + " | by @"+myinfo.username,
                emojis= '❤️',
                webm_sticker = open("file/"+data['video']+'.webm', 'rb')
                )):
            await bot.send_message(message.chat.id, f"Створено новий пак відео-наліпок t.me/addstickers/{data['name_videopack']}_by_{myinfo.username}")
            await state.finish()
            #deletePhoto
            os.remove("file/"+data['video']+'.webm')
'''


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    