import requests


class WB:
    _URL_SUPPLIERS: str = 'https://suppliers-api.wildberries.ru'
    _URL_STATISTICS: str = 'https://statistics-api.wildberries.ru'
    _URL_ADVERT: str = 'https://advert-media-api.wb.ru'
    _URL_RECOMMEND: str = 'https://recommend-api.wildberries.ru'
    _URL_FEEDBACKS: str = 'https://feedbacks-api.wildberries.ru'

    def __init__(self, token: str):
        self._token = token
        self._headers = {'Authorization': f'Bearer {token}'}

    def _api_request__get(self, url: str, params: dict = None):
        if params is None:
            params = {}

        try:
            result = requests.get(
                url=url,
                headers=self._headers,
                params=params
            )
        except Exception as e:
            return {'errors': str(e)}

        try:
            return result.json()
        except (requests.exceptions.JSONDecodeError, requests.exceptions.InvalidJSONError):
            return result.text

    def _api_request__post(self, url: str, data: dict = None):
        if data is None:
            data = {}

        try:
            result = requests.get(
                url=url,
                headers=self._headers,
                json=data
            )
        except Exception as e:
            return {'errors': str(e)}

        try:
            return result.json()
        except (requests.exceptions.JSONDecodeError, requests.exceptions.InvalidJSONError):
            return result.text

    def get_stocks(self, date_from: str):
        """
        Остатки товаров на складах WB. Данные обновляются раз в 30 минут.
        Сервис статистики не хранит историю остатков товаров, поэтому получить данные о них можно только в режиме "на текущий момент".


        Документация: https://openapi.wildberries.ru/statistics/api/ru/#tag/Statistika/paths/~1api~1v1~1supplier~1stocks/get
        """

        url = WB._URL_STATISTICS + '/api/v1/supplier/stocks'
        params = dict(dateFrom=date_from)

        return self._api_request__get(url, params)

    def get_orders(self, date_from: str, flag: int = None):
        """
        Заказы.
        Гарантируется хранение данных не более 90 дней от даты заказа.
        Данные обновляются раз в 30 минут.
        Для идентификации заказа следует использовать поле srid.
        1 строка = 1 заказ = 1 единица товара.

        Документация: https://openapi.wildberries.ru/statistics/api/ru/#tag/Statistika/paths/~1api~1v1~1supplier~1orders/get
        """

        url = WB._URL_STATISTICS + '/api/v1/supplier/orders'
        params = dict(dateFrom=date_from)
        if flag is not None:
            params['flag'] = flag

        return self._api_request__get(url, params)


