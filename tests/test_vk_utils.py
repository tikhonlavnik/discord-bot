from unittest.mock import patch

from utils.vk_utils import Vk


class TestVk:
    def test_check_user_or_group(self):
        with patch("vk_api.VkApi") as mock_vk_api:
            instance = mock_vk_api.return_value
            instance.utils.resolveScreenName.return_value = {"type": "user"}

            result = Vk._Vk__check_user_or_group("test_user")
            assert result == "user"

    def test_get_user_info(self):
        with patch("vk_api.VkApi") as mock_vk_api, patch(
            "requests.get"
        ) as mock_requests_get:
            instance = mock_vk_api.return_value
            instance.users.get.return_value = [
                {"id": 123, "first_name": "Test", "last_name": "User"}
            ]
            mock_response = mock_requests_get.return_value
            mock_response.text = '<ya:created dc:date="2012-11-24T16:19:09+03:00"/>'

            result = Vk._Vk__get_user_info("test_user")
            assert "Пользователь: Да" in result

    def test_get_group_info(self):
        with patch("vk_api.VkApi") as mock_vk_api:
            instance = mock_vk_api.return_value
            instance.groups.getById.return_value = [{"id": 456, "name": "Test Group"}]

            result = Vk._Vk__get_group_info("test_group")
            assert "Группа: Да" in result

    def test_get_vk_entity_info_user(self):
        with patch.object(
            Vk, "_Vk__check_user_or_group", return_value="user"
        ), patch.object(Vk, "_Vk__get_user_info", return_value="Пользователь: Да"):
            result = Vk.get_vk_entity_info("test_user")
            assert "Пользователь: Да" in result

    def test_get_vk_entity_info_group(self):
        with patch.object(
            Vk, "_Vk__check_user_or_group", return_value="group"
        ), patch.object(Vk, "_Vk__get_group_info", return_value="Группа: Да"):
            result = Vk.get_vk_entity_info("test_group")
            assert "Группа: Да" in result
