from rest_framework.pagination import PageNumberPagination


class BasePaginator(PageNumberPagination):
    """Пагинатор для постраничного вывода курсов и уроков"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
