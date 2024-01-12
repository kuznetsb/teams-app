from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 5000
    page_size_query_description = "Number of results to return per page. Send `page_size=max` param for get all items."

    def get_page_size(self, request):
        if self.page_size_query_param:
            if (
                request.query_params.get(self.page_size_query_param, "").lower()
                == "max"
            ):
                return self.max_page_size
        return super().get_page_size(request)
