from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Brand, CarModel, Car

def catalog(request):
    # Получаем все марки
    brands = Brand.objects.all()

    # Получаем параметры из запроса
    brand_id = request.GET.get('brand')
    car_type = request.GET.getlist('type')  # может быть несколько
    price_range = request.GET.get('price')
    search_query = request.GET.get('search', '').strip()

    # Загружаем все машины
    cars = Car.objects.select_related('model__brand').all()

    # Фильтрация по марке
    if brand_id:
        cars = cars.filter(model__brand__id=brand_id)

    # Фильтрация по типу автомобиля
    if car_type:
        cars = cars.filter(car_type__in=car_type)

    # Фильтрация по ценовому диапазону
    if price_range and price_range != 'all':
        try:
            min_price, max_price = map(int, price_range.split('-'))
            cars = cars.filter(price__gte=min_price, price__lte=max_price)
        except ValueError:
            pass  # если пользователь ввел некорректный диапазон вручную

    # Поиск по названию модели или марки (нечувствительно к регистру)
    if search_query:
        cars = cars.filter(
            Q(model__name__icontains=search_query) |
            Q(model__brand__name__icontains=search_query)
        )

    # Сортировка и пагинация
    cars = cars.order_by('model__brand__name', 'model__name')
    paginator = Paginator(cars, 9)  # 9 машин на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Контекст для шаблона
    context = {
        'brands': brands,
        'cars': page_obj,
        'selected_brand': brand_id,
        'selected_types': car_type,
        'selected_price': price_range or 'all',
        'search_query': search_query,
        'page_obj': page_obj,
    }

    return render(request, 'cars/catalog.html', context)
