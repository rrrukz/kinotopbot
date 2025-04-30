from aiogram.dispatcher.filters.state import State, StatesGroup


class KinoState(StatesGroup):
    kino=State()
    kod=State()
    delete_movie=State()



class ReklamaState(StatesGroup):
    reklama=State()
    confirm=State()

class User_delete(StatesGroup):
    id=State()
class Update(StatesGroup):
    update_kino=State()
