from django.http import HttpResponse
import csv

class CsvExporter:
    def export_as_csv(self, request, queryset):
        field_names = self.csv_field_names
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=ucrfva_time_metrics.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response
    export_as_csv.short_description = "Export Selected"