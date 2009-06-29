import operator

from turbion.bits.antispam import Filter

urlpatterns = reduce(
    operator.add,
    [filter.urlpatterns for name, filter in Filter.manager.all() if hasattr(filter, 'urlpatterns')],
    []
)
