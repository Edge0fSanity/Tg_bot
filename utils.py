import asyncio

lifestyle_dict = {"Нет активности":1.2, "Низкая активность":1.375, "Высокая активность":1.65, "Очень высокая активность":1.9}


async def eval_kkal(lifestyle: str, goal: int, age: float, height: float, weight: float, gender: str) -> int:
    """"
        returns int: kkal as per day norm
    """
    kkal = 0
    if gender == "муж":
        kkal = lifestyle_dict[lifestyle]*(66.5+(13.75*weight)+(5.003*height)-(6.775*age))
    else:
        kkal = lifestyle_dict[lifestyle]*(665.1+(9.563*weight)+(1.85*height)-(4.676*age))

    if goal == 2: #Подсчет каллорий взависимости от цели(Набор/снижение массы)
        kkal += kkal * 15 / 100
    elif goal == 0:
        kkal -= kkal * 9 / 100

    return round(kkal)

async def is_float_ru(el:any)-> bool: 
    """
    Проверка числа на то, что его можно преобразовать во float
    вне зависимости от точки или запятой
    """
    if el is None: 
        return False
    try:
        float(el.replace(',', '.', 1))
        return True
    except ValueError:
        return False

async def data_prep(data: dict) -> dict:
    """
    Готовим данные для ввода в sql
    """
    for k in data.keys():
        if await is_float_ru(data[k]):
            data[k] = float(data[k].replace(',', '.', 1))
    return data
