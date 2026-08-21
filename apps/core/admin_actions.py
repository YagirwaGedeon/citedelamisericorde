"""Actions d'administration partagées (export CSV)."""

import csv

from django.http import HttpResponse


def _resolve_attr(obj, dotted_path: str):
    value = obj
    for part in dotted_path.split("."):
        value = getattr(value, part, None)
        if value is None:
            return ""
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if hasattr(value, "url"):
        return value.url
    return value


def export_csv_action(modeladmin, request, queryset, title: str = "export"):
    """Génère un CSV UTF-8 (avec BOM pour Excel) à partir de la sélection."""

    fields = getattr(modeladmin, "csv_export_fields", None)
    if fields is None:
        fields = [f.name for f in queryset.model._meta.concrete_fields]

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{modeladmin.model._meta.model_name}_{title}.csv"'
    response.write("\ufeff")
    writer = csv.writer(response)
    writer.writerow(fields)
    for obj in queryset:
        row = []
        for field_name in fields:
            try:
                value = queryset.model._meta.get_field(field_name).value_from_object(obj)
            except Exception:
                value = _resolve_attr(obj, field_name)
            row.append("" if value is None else str(value))
        writer.writerow(row)
    return response
