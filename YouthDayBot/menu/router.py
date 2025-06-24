from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InputFile, FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from menu.keyboard import week_info_keyboard, main_menu_keyboard, events_keyboard, get_blocks_keyboard
from menu.utils import break_long_message, get_event_text, send_event
from repository.event_repository import EventRepository
from schemas.event import EventSchema, UpdateEventSchema

router = Router()
block_picture = {
    "scene": "picture/block6.jpg",
    "love": "picture/block2.jpg",
    "freedom": "picture/block1.jpg",
    "memory": "picture/block3.jpg",
    "unity": "picture/block4.jpg",
    "move": "picture/block5.jpg",
}

@router.message(Command("test"))
async def test(message: Message):
    await message.answer(text="test", reply_markup=main_menu_keyboard())


@router.message(F.text == "🤹 О неделе молодёжи «Север Молодой»")
async def menu_festival(message: Message):
    text = ("День молодежи в Нижневартовске — это яркий и незабываемый праздник. Гостей ждёт насыщенная программа: "
            "зажигательные концерты с участием местных и приглашённых артистов, спортивные состязания и увлекательные "
            "мастер-классы. На площадках развернутся интерактивные зоны, где каждый сможет проявить свои таланты, "
            "пообщаться с друзьями и зарядиться энергией лета. Но это не просто развлечение — это воплощение ключевых "
            "ценностей Недели Молодёжи: <b>«Память. Любовь. Единство. Свобода. Движение».</b> Они отражают мироощущение "
            "молодёжи, для которой важно сохранять историю, превращать идеи в действия, использовать все возможности "
            "для роста и строить то будущее, в котором хочется жить и творить.\n\nАтмосфера праздника будет наполнена "
            "драйвом и позитивом: громкая музыка, конкурсы с крутыми призами, фуд-зоны с вкусняшками и многое другое. "
            "Это отличная возможность для молодежи города весело провести время, найти новых друзей и получить море "
            "впечатлений. Не пропусти самый яркий день лета — будет жарко🔥")
    break_text = break_long_message(text)
    for msg in break_text:
        await message.answer(msg)


@router.message(F.text == "📆 Программа недели")
async def menu_week_program(message: Message):
    await message.answer(text="Выберите необходимую функцию", reply_markup=week_info_keyboard())


@router.message(F.text == "◀️ Назад")
async def menu_return(message: Message):
    await message.answer(text="Чем я могу помочь?", reply_markup=main_menu_keyboard())


@router.message(F.text == "🗓️ Полное расписание")
async def full_menu(message: Message):
    images = ["picture/week1.jpg", "picture/week2.jpg", "picture/week3.jpg"]
    media = MediaGroupBuilder()
    for image in images:
        image = FSInputFile(path=image)
        media.add_photo(media=image)
    await message.answer_media_group(media=media.build())


@router.message(F.text == "📜 Узнать подробно")
async def menu_events(message: Message):
    keyboard = await events_keyboard()
    await message.answer(text="Выберите мероприятие", reply_markup=keyboard.as_markup())


@router.message(F.text == "🥳 День Молодёжи - 2025")
async def menu_day(message: Message, bot: Bot):
    photo = FSInputFile(path="picture/youth_day.jpg")
    await message.answer_photo(photo=photo)
    await message.answer(text="Выберите площадку", reply_markup=get_blocks_keyboard())

@router.callback_query(F.data.startswith("block_"))
async def block_info(callback: CallbackQuery):
    await callback.answer()
    block_name = callback.data.split("_")[1]
    picture_path = block_picture[block_name]
    picture = FSInputFile(path=picture_path)
    await callback.message.delete()
    await callback.message.answer_photo(photo=picture, reply_markup=get_blocks_keyboard())


@router.message(F.text == "🎟️ О розыгрыше")
async def menu_lottery(message: Message):
    text = ("Готов урвать главные призы этого лета? 🔥 Молодёжный центр разыграет среди подписчиков своего "
            "Telegram-канала (@molodnv) невероятные награды:\n\n🏆 Годовой запас пиццы – целый год вкусных угощений. От "
            "ДоДо Пиццы – где самая вкусная, сочная, пицца Нижневартовска. И не только пицца!\n🎧 AirPods Max 2 Premium "
            "– стильные наушники с премиум-звуком. От наших партнеров  KingStore - огромный выбор техники разных "
            "брендов по самым приятным ценам.\n\nРозыгрыш пройдёт 28 июня на главной сцене во время празднования Дня "
            "молодёжи. Условия просты: \n✔ Будь подписан на наш Telegram-канал; \n✔ Приходи на праздник – победителей "
            "объявим прямо со сцены. \n\nЧем больше друзей приведёшь – тем выше шансы. Следи за анонсами, участвуй и "
            "забирай топовые призы. Это твой шанс – не упусти 🚀✨")

    break_text = break_long_message(text)
    for msg in break_text:
        await message.answer(msg)


@router.message(F.text == "✉️ Связь с организатором")
async def menu_contact(message: Message):
    text = "Остались вопросы или есть крутые идеи для мероприятий? Свяжись с командой организаторов – мы всегда на связи!\nПиши сообщение в сообщество, и мы тебе ответим на твой вопрос.\n\nВКонтакте: https://vk.com/molodday2025?from=groups"
    await message.answer(text=text)


@router.callback_query(F.data.startswith("event_page_"))
async def menu_events_forward(callback: CallbackQuery):
    await callback.answer()
    page = int(callback.data.split("_")[2])
    keyboard = await events_keyboard(page=page)
    await callback.message.edit_reply_markup(reply_markup=keyboard.as_markup())


@router.callback_query(F.data.startswith("event_"))
async def get_event(callback: CallbackQuery, repository=EventRepository()):
    await callback.answer()
    await callback.message.delete()
    id = int(callback.data.split("_")[1])
    event = await repository.get_one(id)
    event = EventSchema.from_orm(event)
    await send_event(event, callback)
    event_update = UpdateEventSchema(
        views=event.views + 1
    )
    await repository.update(event_id=event.id, event_data=event_update)
