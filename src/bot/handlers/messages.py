from src.applications.models import STATUS_MAP, TYPE_MAP
from src.promo_codes import DiscountType

MESSAGES = {
    "ru": {
        "user_start_message": "Привет путник!\nЯ помогу тебе починить твой мот!",
        "new_user_start_message": "Привет путник! Я помогу тебе починить твой мот! Для начала давай познакомимся.",
        "help": (
            "Вот список команд, которые я понимаю:\n"
            "/start - начать работу со мной\n"
            "/help - показать это сообщение\n"
            "/profile - показать информацию о тебе\n"
        ),
        "admin_start_message": "Привет, админ!",
        "worker_start_message": "Привет сервисмен!",
        "profile": lambda name, phone_number: (
            f"👤 Ваш профиль:\nИмя: {name}\nТелефон: {phone_number}"
        ),
        "motorcycle": lambda motorcycle_model, year: (
            f"🏍️ Мотоцикл:\nМодель: {motorcycle_model}\nГод выпуска: {year}\n"
        ),
        "fallback_message": (
            "Упс! Я не понимаю, что ты имеешь в виду. Пожалуйста, используй команды или напиши /help для получения помощи."
        ),
        "back_to_start": "Чем я могу помочь тебе? Выбери действие из меню ниже",
        "register_name": "Как тебя зовут?",
        "register_phone_number": "Поделитесь вашим номером телефона, нажав на кнопку ниже, или напишите его в обычном формате (например, 89017856745 или 79055943758)",
        "not_valid_phone_number": "Введите корректный номер телефона!",
        "could_not_find_user": "К сожалению, не удалось найти профиль. Попробуйте позже.",
        "edit_name_process": lambda name: f"Ваше текущее имя: {name}\nНапиши новое имя или оставь без изменений, нажав на кнопку ниже.",
        "edit_phone_number_process": lambda phone_number: f"Ваш текущий номер телефона: {phone_number}\nВведите новый номер телефона или нажмите кнопку ниже для отправки контакта или для того, чтобы оставить номер телефона без изменения.",
        "edit_motorcycle_model_process": lambda motorcycle_model: f"Текущая модель мотоцикла: {motorcycle_model}\nНапиши новую модель мотоцикла (например, Harley-Davidson Sportster) или оставь без изменений, нажав на кнопку ниже.",
        "edit_motorcycle_year_process": lambda year: f"Текущий год выпуска: {year}\nНапиши новый год выпуска мотоцикла (например, 2020) или оставь без изменений, нажав на кнопку ниже.",
        "error_user_update": "Произошла ошибка при обновлении пользователя, пожалуйста, попробуйте позже",
        "add_motorcycle_model_process": "Давай начнем добавление твоего мотоцикла в гараж.\nНапиши мне его модель (например, Harley-Davidson Sportster)",
        "add_motorcycle_year_process": "Отлично! Теперь напиши год выпуска мотоцикла (например, 2020)",
        "not_valid_year": "Пожалуйста, введи корректный год выпуска (например, 2020).",
        "add_motorcycle_error": "Произошла ошибка при добавлении мотоцикла, пожалуйста, попробуйте позже",
        "edit_motorcycle_error": "Произошла ошибка при обновлении мотоцикла, пожалуйста, попробуйте позже",
        "delete_motorcycle_error": "К сожалению, не получилось удалить мотоцикл, попробуйте позже.",
        "delete_motorcycle_successful": "Мотоцикл успешно удален!",
        "garage_is_empty": "Упсс, у вас пока что нет мотоциклов. Самое время добавить новый мотоцикл!",
        "garage": "Добро пожаловать в ваш гараж! Здесь вы можете управлять своими мотоциклами.",
        "motorcycle_not_found_error": "К сожалению, не удалось найти мотоцикл. Попробуйте позже.",
        "choose_date_for_application_service": "Выберите дату для записи в сервисный центр",
        "choose_time_for_application_service": "Выберите время для записи в сервисный центр",
        "choose_motorcycle_for_application_service": "Выберите мотоцикл для записи в сервисный центр",
        "choose_motorcycle_for_application_evacuation": "Выберите мотоцикл, который нужно эвакуировать",
        "description_for_application_service": "Опишите проблему с мотоциклом или услугу, которую вы хотите получить",
        "send_media_for_application_service": "Прикрепите фото или видео, если это необходимо, иначе пропустите этот шаг",
        "media_for_application_service_not_valid": "Прикрепите фото или видео, иначе пропустите этот шаг",
        "photo_result_not_valid": "Отправьте фото результата работы по заявке",
        "promo_code_for_application_service": "Если у вас есть промокод, введите его здесь, иначе пропустите этот шаг",
        "not_found_promo_code": "Введенный вами промокод недействительный или не существует, проверьте, что вы написали его правильно",
        "create_application_error": "Произошла ошибка при создании заявки, попробуйте позже",
        "skip_date": "Выберите конкретное время",
        "old_date": "Данное время уже в прошлом)",
        "location_for_application_evacuation": "Отправьте свое местоположение. Для этого нажмите на кнопку ниже, чтобы отправить вашу текущую локацию, или отправьте свое местоположение вручную, как вложение телеграм. Если у вас не получается отправить местоположение, просто напишите адрес, где находится мотоцикл.",
        "description_for_application_evacuation": "Опишите проблему с мотоциклом",
        "application": lambda motorcycle_model,
        description,
        service_datetime,
        status: f"<b>Заявка в сервисный центр</b>:\nМотоцикл: {motorcycle_model}\nОписание: {description}\nВремя: {service_datetime.strftime('%d-%m-%Y %H:%M')}\nСтатус: {STATUS_MAP[status]}",
        "application_evacuation": lambda motorcycle_model,
        description,
        status,
        address: f"<b>Заявка на эвакуацию:</b>\nМотоцикл: {motorcycle_model}\nОписание: {description}\nСтатус: {STATUS_MAP[status]}"
        + (f"\nАдрес: {address}" if address else ""),
        "cancel_application_error": "Не удалось отменить заявку",
        "cancel_application_successful": "Заяка успешно отменена",
        "create_application_evacuation_successful": "Ваша заявка успешно создана, мы уже спешим к вам на помощь!",
        "admin_settings_menu": "Вы в настройках администратора. Здесь вы можете изменить максимальное количество записей и режим работы, а также исключить некоторые даты, которые хотите сдлеать нерабочими.",
        "admin_max_records": lambda max_records: f"На текущий момент максимальное число записей: {max_records}.\nВведите новое число или оставьте без изменений, нажав на кнопку ниже.",
        "admin_operating_mode": lambda operating_mode: f"На текущий момент рабочее время: {operating_mode}.\nВведите новое рабочее время в нужном формате (например, 10-20) или оставьте без изменений, нажав на кнопку ниже.",
        "admin_excluded_dates": "Введите даты, которые вы хотите исключить из рабочего времени через запятую (например, 01.01.2024, 02.01.2024), или поставьте прочерк (-), чтобы оставить без изменений.",
        "invalid_max_records": "Пожалуйста, введите корректное число (например, 10).",
        "invalid_operating_mode": "Введите корректный промежуток",
        "admin_operating_mode_saved": lambda operating_mode: f"Теперь рабочее время: {operating_mode}.",
        "admin_max_records_saved": lambda max_records: f"Теперь максимальное число записей: {max_records}.",
        "invalid_excluded_dates": "Пожалуйста, введите корректные даты в формате ДД.ММ.ГГГГ через запятую (например, 01.01.2024, 02.01.2024).",
        "admin_excluded_dates_saved": lambda excluded_dates: f"Добавлены выходные: {excluded_dates}.",
        "manage_roles_menu": "Вы в меню управления ролями. Здесь вы можете добавить админа или работника, а также вернуться в главное меню.",
        "add_admin_username_process": "Введите имя пользователя (например, @admin_username), которого вы хотите добавить в администраторы. Важно, чтобы пользователь был зарегистрирован в боте.",
        "add_worker_username_process": "Введите имя пользователя (например, @worker_username), которого вы хотите добавить в работники. Важно, чтобы пользователь был зарегистрирован в боте.",
        "error_adding_admin": "Произошла ошибка при добавлении администратора, пожалуйста, попробуйте позже.",
        "error_adding_worker": "Произошла ошибка при добавлении работника, пожалуйста, попробуйте позже.",
        "user_not_found": lambda username: f"Не удалось найти пользователя с именем @{username}, проверьте, что вы написали его правильно.",
        "admin_role_added": lambda username: f"Администратор @{username} успешно добавлен!",
        "worker_role_added": lambda username: f"Специалист @{username} успешно добавлен!",
        "new_admin_role_notification": "Вас назначили администратором! Вам доступна админ панель!",
        "new_worker_role_notification": "Вас назначили специалистом! Вам доступна панель работника!",
        "start_create_promo_code": "Супер! Давай начнем добавление нового промокода.\nНапиши мне код промокода (например, SUMMER2025)",
        "discount_promo_code_process": "Суперский промокод! Теперь напиши размер скидки (есть два вида: в процентах или в рублях).\nЕсли ты хочешь сделать промокод с фиксированной скидкой (в рублях), просто напиши сумму без знака процента. Например: 25% или 1000.",
        "promo_codes_menu": "Вы в меню управления промокодами. Здесь вы можете создавать, просматривать и управлять промокодами.",
        "no_promo_codes": "Пока что нет промокодов, вы можете создать новый промокод, нажав на кнопку ниже.",
        "promo_code": lambda code: f"Промокод: {code.code}\n"
        f"Скидка: {int(code.discount_value)}{'%' if code.discount_type == DiscountType.PERCENTAGE else ' руб.'}\n"
        f"Количество использований: {code.used_count}\n",
        "promo_code_discount_value_error": "Пожалуйста, введи корректный размер скидки. Если это процент, напиши с символом '%', например: 25%. Если это фиксированная сумма, просто укажи число, например: 1000.",
        "promo_code_start_date_process": "Отлично! Теперь напиши с какого времени будет действовать промокод (например, 30.07.2025 12:30 или 30.07.2025 (в таком случае промокод начнет действовать с начала дня)) или поставь -, если промокод не должен иметь начала действия",
        "promo_code_date_error": "Пожалуйста, введи корректную дату в формате ДД.ММ.ГГГГ ЧЧ:ММ или ДД.ММ.ГГГГ, либо поставьте -",
        "promo_code_end_date_process": "Хорошо! Теперь напиши до какого времени будет действовать промокод (например, 30.07.2025 12:30 или 30.07.2025 (в таком случае промокод будет действовать до 29.07.2025 23:59)) или поставь -, если промокод не должен иметь конца действия",
        "promo_code_usage_limit_process": "Отлично! Теперь можно указать лимит на количество использований промокода (например, 300 (в таком случае промокодом смогут воспользоваться первые 300 клиентов)) или поставьте -, тогда не будет ограничений на количество использований промокода",
        "promo_code_usage_limit_error": "Пожалуйста, введи корректное число (например, 234).",
        "promo_code_usage_limit_negative_error": "Пожалуйста, убедись, что ты ввел корректное ограничение. PS: Ограничение не может быть меньше 0!",
        "promo_code_created_error": "Произошла ошибка при создании промокода, попробуйте позже",
        "promo_code_created_successful": "Промокод успешно создан!",
        "promo_code_delete_error": "Произошла ошибка при удалении промокода, попробуйте позже",
        "promo_code_delete_successful": "Промокод успешно удален!",
        "promo_code_not_found": "К сожалению, не удалось найти промокод. Попробуйте позже.",
        "edit_promo_code_start": lambda code: f"Текущий код: {code}\nНапиши новый код (например, SUM25) или оставь без изменений, нажав на кнопку ниже.",
        "edit_promo_code_discount": lambda discount_value,
        discount_type: f"Текущая скидка: {discount_value}{'%' if discount_type == DiscountType.PERCENTAGE else ''}\n"
        f"Напиши новую скидку. Если ты хочешь сделать промокод с фиксированной скидкой (в рублях), просто напиши сумму без знака процента. Например: 25% или 1000. Если же хочешь ставить без изменений, то нажми на кнопку ниже.",
        "edit_promo_code_valid_from": lambda valid_from: (
            f"Сейчас промокод действует с {valid_from.strftime('%d.%m.%Y %H:%M')}. "
            if valid_from
            else "Сейчас промокод не имеет начала действия. "
        )
        + "Укажи новое начало действия промокода (например, 30.07.2025 12:30 или 30.07.2025 (в таком случае промокод начнет действовать с начала дня)) или поставь -, если промокод не должен иметь начала действия, или оставь без изменений, нажав на кнопку ниже.",
        "edit_promo_code_valid_until": lambda valid_until: (
            f"Сейчас промокод действует до {valid_until.strftime('%d.%m.%Y %H:%M')}. "
            if valid_until
            else "Сейчас промокод не имеет окончания действия. "
        )
        + "Укажи новый конец действия промокода (например, 30.07.2025 12:30 или 30.07.2025 (в таком случае промокод начнет действовать с начала дня)) или поставь -, если промокод не должен иметь конца действия, или оставь без изменений, нажав на кнопку ниже.",
        "edit_promo_code_usage_limit": lambda usage_limit: f"Сейчас лимит использования промокода: {usage_limit if usage_limit is not None else 'нет ограничений'}\nУкажи новый лимит на количество использований промокода (например, 300 (в таком случае промокодом смогут воспользоваться первые 300 клиентов)) или поставь -, тогда не будет ограничений на количество использований промокода, или оставь без изменений, нажав на кнопку ниже.",
        "promo_code_update_error": "Произошла ошибка при обновлении промокода, пожалуйста, попробуйте позже",
        "edit_promo_code_successful": "Промокод успешно обновлен!",
        "admin_excluded_dates_skipped": "Вы не указали даты, которые нужно исключить из рабочего времени. Даты не были изменены.",
        "promo_code_added_successfully": "Промокод успешно применен!",
        "new_application_notification_for_admin": lambda application,
        user,
        motorcycle,
        promo_code: (
            f"Новая заявка в сервисный центр:\n"
            f"Клиент: {user.name} @{user.username} <code>{user.phone_number}</code>\n"
            f"Мотоцикл: {motorcycle.motorcycle_model} ({motorcycle.year})\n"
            f"Описание: {application.description}\n"
            f"Дата и время: {application.service_datetime.strftime('%d-%m-%Y %H:%M')}\n"
            f"Промокод: {promo_code.code if promo_code else '-'}\n"
        ),
        "assigned_application_notification_for_admin": lambda application,
        user,
        motorcycle,
        promo_code,
        worker: (
            f"Заявка в сервисный центр:\n"
            f"Статус: {STATUS_MAP[application.status]}\n"
            f"Специалист: {worker.name} @{worker.username}\n"
            f"Клиент: {user.name} @{user.username} <code>{user.phone_number}</code>\n"
            f"Мотоцикл: {motorcycle.motorcycle_model} ({motorcycle.year})\n"
            f"Описание: {application.description}\n"
            f"Дата и время: {application.service_datetime.strftime('%d-%m-%Y %H:%M')}\n"
            f"Промокод: {promo_code.code if promo_code else '-'}\n"
            f"Комментарий администратора: {application.admin_comment if application.admin_comment else '-'}"
        ),
        "in_progress_application_notification_for_admin": lambda application,
        user,
        motorcycle,
        promo_code: (
            f"Специалист взял в работу данную заявку:\n"
            f"Статус: {STATUS_MAP[application.status]}\n"
            f"Клиент: {user.name} @{user.username} <code>{user.phone_number}</code>\n"
            f"Мотоцикл: {motorcycle.motorcycle_model} ({motorcycle.year})\n"
            f"Описание: {application.description}\n"
            f"Дата и время: {application.service_datetime.strftime('%d-%m-%Y %H:%M')}\n"
            f"Промокод: {promo_code.code if promo_code else '-'}\n"
        ),
        "completed_application_notification_for_admin": lambda application,
        user,
        motorcycle,
        promo_code: (
            f"Специалист выполнил работу по заявке:\n"
            f"Статус: {STATUS_MAP[application.status]}\n"
            f"Клиент: {user.name} @{user.username} <code>{user.phone_number}</code>\n"
            f"Мотоцикл: {motorcycle.motorcycle_model} ({motorcycle.year})\n"
            f"Описание: {application.description}\n"
            f"Дата и время: {application.service_datetime.strftime('%d-%m-%Y %H:%M')}\n"
            f"Промокод: {promo_code.code if promo_code else '-'}\n"
        ),
        "assigned_application_notification_for_worker": lambda application,
        user,
        motorcycle,
        promo_code: (
            f"Заявка в сервисный центр:\n"
            f"Статус: {STATUS_MAP[application.status]}\n"
            f"Клиент: {user.name} @{user.username} <code>{user.phone_number}</code>\n"
            f"Мотоцикл: {motorcycle.motorcycle_model} ({motorcycle.year})\n"
            f"Описание: {application.description}\n"
            f"Дата и время: {application.service_datetime.strftime('%d-%m-%Y %H:%M')}\n"
            f"Промокод: {promo_code.code if promo_code else '-'}\n"
            f"Комментарий администратора: {application.admin_comment if application.admin_comment else '-'}"
        ),
        "assigned_application_notification_for_user": lambda application, motorcycle, promo_code: (
            f"Заявка в сервисный центр:\n"
            f"Статус: {STATUS_MAP[application.status]}\n"
            f"Мотоцикл: {motorcycle.motorcycle_model} ({motorcycle.year})\n"
            f"Описание: {application.description}\n"
            f"Дата и время: {application.service_datetime.strftime('%d-%m-%Y %H:%M')}\n"
            f"Промокод: {promo_code.code if promo_code else '-'}\n"
        ),
        "completed_application_notification_for_user": lambda application, motorcycle, promo_code: (
            f"Ваш мотоцикл готов, заберите в удобное вам время:\n"
            f"Статус: {STATUS_MAP[application.status]}\n"
            f"Мотоцикл: {motorcycle.motorcycle_model} ({motorcycle.year})\n"
            f"Описание: {application.description}\n"
            f"Дата и время: {application.service_datetime.strftime('%d-%m-%Y %H:%M')}\n"
            f"Промокод: {promo_code.code if promo_code else '-'}\n"
        ),
        "application_cancelled_notification_for_worker": lambda application,
        user,
        motorcycle,
        promo_code: (
            f"Заявка была отменена администратором:\n"
            f"Статус: {STATUS_MAP[application.status]}\n"
            f"Клиент: {user.name} @{user.username} <code>{user.phone_number}</code>\n"
            f"Мотоцикл: {motorcycle.motorcycle_model} ({motorcycle.year})\n"
            f"Описание: {application.description}\n"
            f"Дата и время: {application.service_datetime.strftime('%d-%m-%Y %H:%M')}\n"
            f"Промокод: {promo_code.code if promo_code else '-'}\n"
        ),
        "application_cancelled_notification_for_user": lambda application, motorcycle, promo_code: (
            f"Ваша заявка была отменена администратором:\n"
            f"Статус: {STATUS_MAP[application.status]}\n"
            f"Мотоцикл: {motorcycle.motorcycle_model} ({motorcycle.year})\n"
            f"Описание: {application.description}\n"
            f"Дата и время: {application.service_datetime.strftime('%d-%m-%Y %H:%M')}\n"
            f"Промокод: {promo_code.code if promo_code else '-'}\n"
        ),
        "application_user_cancelled_notification_for_admin": lambda application,
        user,
        motorcycle,
        promo_code: (
            f"Заявка была отменена пользователем:\n"
            f"Статус: {STATUS_MAP[application.status]}\n"
            f"Клиент: {user.name} @{user.username} <code>{user.phone_number}</code>\n"
            f"Мотоцикл: {motorcycle.motorcycle_model} ({motorcycle.year})\n"
            f"Описание: {application.description}\n"
            f"Дата и время: {application.service_datetime.strftime('%d-%m-%Y %H:%M')}\n"
            f"Промокод: {promo_code.code if promo_code else '-'}\n"
        ),
        "application_user_cancelled_notification_for_worker": lambda application,
        user,
        motorcycle,
        promo_code: (
            f"Заявка была отменена пользователем:\n"
            f"Статус: {STATUS_MAP[application.status]}\n"
            f"Клиент: {user.name} @{user.username} <code>{user.phone_number}</code>\n"
            f"Мотоцикл: {motorcycle.motorcycle_model} ({motorcycle.year})\n"
            f"Описание: {application.description}\n"
            f"Дата и время: {application.service_datetime.strftime('%d-%m-%Y %H:%M')}\n"
            f"Промокод: {promo_code.code if promo_code else '-'}\n"
        ),
        "application_not_found": "К сожалению, не удалось найти заявку. Попробуйте позже.",
        "worker_not_found": "К сожалению, не удалось найти специалиста. Попробуйте позже.",
        "assign_application_error": "Произошла ошибка при назначении специалиста на заявку. Попробуйте позже.",
        "status_update_error": "Произошла ошибка при обновлении статуса заявки. Попробуйте позже.",
        "status_updated_successfully": "Статус заявки успешно обновлен!",
        "evacuation_application_notification_for_admin": lambda application, user, motorcycle: (
            f"Заявка на эвакуацию:\n"
            f"Клиент: {user.name} @{user.username} <code>{user.phone_number}</code>\n"
            f"Мотоцикл: {motorcycle.motorcycle_model} ({motorcycle.year})\n"
            f"Описание: {application.description}\n"
            f"Статус: {STATUS_MAP[application.status]}"
        )
        + (f"\nАдрес: {application.location}" if application.location else ""),
        "evacuation_cancel_admin": "К сожалению, ваша заявка была отклонена администратором.",
        "evacuation_cancel_notification_for_admin": lambda application, user, motorcycle: (
            f"Заявка на эвакуацию, была отменена пользователем:\n"
            f"Клиент: {user.name} @{user.username} <code>{user.phone_number}</code>\n"
            f"Мотоцикл: {motorcycle.motorcycle_model} ({motorcycle.year})\n"
            f"Описание: {application.description}\n"
            f"Статус: {STATUS_MAP[application.status]}"
        )
        + (f"\nАдрес: {application.location}" if application.location else ""),
        "evacuation_in_progress": lambda motorcycle_model, description, status, location: (
            f"<b>К вам спешат на помощь:</b>\n"
            f"Мотоцикл: {motorcycle_model}\n"
            f"Описание: {description}\n"
            f"Статус: {STATUS_MAP[status]}" + (f"\nАдрес: {location}" if location else "")
        ),
        "evacuation_completed": lambda motorcycle_model, description, status, location: (
            f"<b>Ваша заявка выполнена:</b>\n"
            f"Мотоцикл: {motorcycle_model}\n"
            f"Описание: {description}\n"
            f"Статус: {STATUS_MAP[status]}" + (f"\nАдрес: {location}" if location else "")
        ),
        "application_created_successful": "Заявка была успешно создана!",
        "admin_contacts_information": lambda contacts: (
            f"📞 Контакты:\n"
            f"Имя: {contacts['name']}\n"
            f"Телефон: <code>{contacts['phone']}</code>\n"
            f"TG: {contacts['username']}\n"
        ),
        "admin_tg": lambda username: f"Или свяжитесь через телеграм: {username}",
        "admin_edit_phone_contact": lambda phone: f"Текущий номер телефона для связи с пользователями: <code>{phone}</code>\nВведите новый номер телефона или оставьте без изменений, нажав на кнопку ниже.",
        "admin_edit_username_contact": lambda username: f"Текущий username для связи с пользователями: {username}\nВведите новый username (@example_username) или оставьте без изменений, нажав на кнопку ниже.",
        "admin_edit_name_contact": lambda name: f"Текущее имя для связи с пользователями: {name}\nВведите новое имя или оставьте без изменений, нажав на кнопку ниже.",
        "list_admins_and_workers": lambda admins,
        workers: f"Админы:\n{'\n'.join(f'@{admin.username}' for admin in admins)}\n\n"
        f"Работники:\n{'\n'.join(f'@{worker.username}' for worker in workers)}",
        "no_applications_last_2_weeks": "За последние две недели не было ни одной заявки",
        "application_info": lambda application, worker, user, motorcycle, promo_code: (
            f"Заявка №{application.number}\n"
            f"Статус: {STATUS_MAP[application.status]}\n"
            f"Тип заявки: {TYPE_MAP[application.type]}\n"
            f"Мотоцикл: {motorcycle.motorcycle_model} ({motorcycle.year})\n"
            f"Клиент: {user.name} @{user.username} <code>{user.phone_number}</code>\n"
            f"Описание: {application.description or 'Нет описания'}\n"
            f"Промокод: {promo_code.code if promo_code else '-'}\n"
            f"Специалист: {f'{worker.name} @{worker.username}' if worker else '-'}"
        ),
        "add_admin_comment": "Добавьте комментарий для специалиста или нажмите пропустить",
        "admin_comment_has_been_added": "Вы успешно добавили комментарий",
        "add_admin_comment_error": "К сожалению, во время добавления комментария произошла ошибка",
        "add_photo_result": "Прикрепите фото результата работы",
    },
    # "en": {...},
}
