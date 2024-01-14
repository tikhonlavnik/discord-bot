from datetime import datetime
import requests

import vk_api
from bs4 import BeautifulSoup
from config import Config


class Vk:
    """
    Class for getting VK users and communities info
    """

    __vk_session = vk_api.VkApi(token=Config.VK_TOKEN)
    __vk = __vk_session.get_api()
    __user_fields = ["photo_max_orig", "screen_name"]
    __group_fields = ["photo_max_orig"]

    @classmethod
    def __check_user_or_group(cls, entity_name: str) -> str:
        response = cls.__vk.utils.resolveScreenName(screen_name=entity_name)
        return response.get("type")

    @classmethod
    def __get_user_info(cls, username: str) -> str:
        user_info = cls.__vk.users.get(user_ids=username, fields=cls.__user_fields)[0]
        user_info["registration_date"] = cls.__get_user_registration_date(
            user_info.get("id")
        )
        return cls.__create_user_answer_string(user_info)

    @classmethod
    def __get_group_info(cls, group_name: str) -> str:
        group_info = cls.__vk.groups.getById(
            group_ids=group_name, fields=cls.__group_fields
        )[0]
        return cls.__create_group_answer_string(group_info)

    @staticmethod
    def __get_user_registration_date(user_id: int):
        response = requests.get(f"https://vk.com/foaf.php?id={user_id}")
        xml = response.text
        soup = BeautifulSoup(xml, "lxml")
        created = soup.find("ya:created").get("dc:date")
        formatted_date = datetime.strptime(created, "%Y-%m-%dT%H:%M:%S%z").strftime(
            "%d.%m.%Y"
        )
        return formatted_date

    @staticmethod
    def __create_user_answer_string(user_info: dict) -> str:
        return f"""
Пользователь: Да
Linkname: {user_info.get("screen_name")}
Имя пользователя: {user_info.get("first_name")} {user_info.get("last_name")}
ID: {user_info.get("id")}
Дата регистрации: {user_info.get("registration_date") or "Not found"}
Фото: {user_info.get("photo_max_orig")}
                """

    @staticmethod
    def __create_group_answer_string(group_info: dict) -> str:
        return f"""
Группа: Да
Linkname: {group_info.get("screen_name")}
Название группы: {group_info.get("name")}
ID: {group_info.get("id")}
Фото: {group_info.get("photo_max_orig")}
                """

    @classmethod
    def get_vk_entity_info(cls, entity_name: str) -> str:
        entity_type = cls.__check_user_or_group(entity_name)

        if entity_type.lower() == "user":
            return cls.__get_user_info(entity_name)
        elif entity_type.lower() == "group":
            return cls.__get_group_info(entity_name)
