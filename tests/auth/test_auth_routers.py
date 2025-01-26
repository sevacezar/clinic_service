""""Module with auth API-tests"""

from typing import Any
from httpx import AsyncClient, Response


class TestAuthAPI:
    """Class with tests of operations with auth."""

    async def test_login_success(
            self,
            client: AsyncClient,
            test_user_not_doctor: dict[str, Any],
    ):
        """Test success user login"""
        login_data: dict[str, str] = {
            'username': test_user_not_doctor.get('username'),
            'password': test_user_not_doctor.get('password'),
        }
        response: Response = await client.post(
            url='/login',
            json=login_data,
        )

        assert response.status_code == 200
        assert 'token' in response.json()

    async def test_login_user_not_found(
            self,
            client: AsyncClient,
    ):
        """Test login user not found"""
        login_data: dict[str, str] = {
            'username': 'john72',
            'password': 'qwerty',
        }
        response: Response = await client.post(
            url='/login',
            json=login_data,
        )

        assert response.status_code == 401
        assert 'detail' in response.json()
        assert response.json().get('detail') == 'Invalid credentials!'

    async def test_login_user_invalid_password(
            self,
            client: AsyncClient,
            test_user_not_doctor: dict[str, Any],
    ):
        """Test login user invalid password"""
        login_data: dict[str, str] = {
            'username': test_user_not_doctor.get('username'),
            'password': 'invalid_password',
        }
        response: Response = await client.post(
            url='/login',
            json=login_data,
        )

        assert response.status_code == 401
        assert 'detail' in response.json()
        assert response.json().get('detail') == 'Invalid credentials!'
