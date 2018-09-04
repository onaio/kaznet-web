"""
Remnderers module
"""
import csv
from rest_framework_csv.misc import Echo
from rest_framework_csv.renderers import CSVRenderer


class CSVStreamingRenderer(CSVRenderer):
    """
    Based on rest_framework_csv.renderers.CSVStreamingRenderer,
    tabilize() call is not iterator-friendly.
    """

    def render(self, data, media_type=None, renderer_context={}):
        """
        Prepare and render response
        """
        try:
            queryset = data['queryset']
            serializer = data['serializer']
            context = data['context']
        except KeyError:
            return None

        csv_buffer = Echo()
        csv_writer = csv.writer(csv_buffer)

        header_fields = list()
        for item in queryset:
            # yield the headers
            if len(header_fields) < 1:
                header_fields = list(serializer(item, context=context).fields)
                yield csv_writer.writerow(header_fields)
            # yield the actual data
            items = serializer(item, context=context).data
            ordered = [items[column] for column in header_fields]
            yield csv_writer.writerow([
                elem for elem in ordered
            ])
