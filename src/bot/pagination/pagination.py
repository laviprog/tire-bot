from aiogram.filters.callback_data import CallbackData


class DatePagination(CallbackData, prefix="date"):
    day: int
