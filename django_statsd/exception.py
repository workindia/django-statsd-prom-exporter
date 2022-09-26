class DjangoStatsdConfigurationMissingException(Exception):
    def __init__(self, exporter_alias: str, *args: object) -> None:
        self.exporter_alias = exporter_alias
        super().__init__(*args)

    def __str__(self):
        return (
            f'HOST, PORT configuration is missing for exporter_alias: {self.exporter_alias} in django settings.'
            ' Django-Statsd cannot work without these settings.'
        )
