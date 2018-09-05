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

    # pylint: disable=arguments-differ
    def render(
            self, data: dict,
            media_type: str = None,
            renderer_context: dict = dict):
        """
        Prepare and render response
        """
        try:
            queryset = data['queryset']
            serializer = data['serializer']
            context = data['context']
        except KeyError:
            yield None
        else:
            csv_buffer = Echo()
            csv_writer = csv.writer(csv_buffer)

            header_fields = list()
            for item in queryset:
                # yield the headers
                if not header_fields:
                    header_fields = list(
                        serializer(item, context=context).fields)
                    yield csv_writer.writerow(header_fields)
                # yield the actual data
                items = serializer(item, context=context).data
                ordered = [items[column] for column in header_fields]
                yield csv_writer.writerow(ordered)
