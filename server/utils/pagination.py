from rest_framework.pagination import PageNumberPagination


# 自行設定 page size
class PageNumberWithSizePagination(PageNumberPagination):
    page_size_query_param = "page_size"  # 使用者可以指定
    max_page_size = 1000  # 一定要設定最大值 以防使用者

    def paginate_queryset(self, queryset, request, view=None):
        # view is not None
        # getattr(view, "page_size",None) 去view中尋找有沒有page_size的資料 如果沒有就存取None
        # page_size is int
        if (
            view is not None
            and (page_size := getattr(view, "page_size", None))
            and isinstance(page_size, int)
        ):
            self.page_size = page_size

        return super().paginate_queryset(queryset, request, view)
