from aiogram.filters.callback_data import CallbackData


class DatePagination(CallbackData, prefix="date"):
    date: str

class TimePagination(CallbackData, prefix="time"):
    date: str
