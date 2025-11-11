from django.core.paginator import Paginator

def paginate(request, queryset, per_page=5):
    """
    Функция для пагинации списка объектов.
    
    :param request: Объект HttpRequest.
    :param queryset: QuerySet или список объектов для пагинации.
    :param per_page: Количество объектов на одной странице.
    :return: Словарь с 'page_obj' и 'custom_page_range' для контекста шаблона.
    """
    
    paginator = Paginator(queryset, per_page)
    
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    current_page_num = page_obj.number
    page_range = paginator.page_range
    num_neighbors = 2
    
    start_index = max(1, current_page_num - num_neighbors - 1)
    end_index = min(paginator.num_pages, current_page_num + num_neighbors)
    
    custom_page_range = list(page_range[start_index:end_index])

    show_first_ellipsis = start_index > 1
    show_last_ellipsis = end_index < paginator.num_pages

    if show_first_ellipsis:
        custom_page_range.insert(0, '...')
        custom_page_range.insert(0, 1)

    if show_last_ellipsis:
        custom_page_range.append('...')
        custom_page_range.append(paginator.num_pages)

    return {
        'page_obj': page_obj,
        'custom_page_range': custom_page_range,
    }