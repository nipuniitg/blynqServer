from django.core.serializers.python import Serializer

from customLibrary.views_lib import mail_exception


class CitySerializer(Serializer):
    def end_object( self, obj ):
        try:
            self._current['city_id'] = obj._get_pk_val()
            self.objects.append( self._current )
        except Exception as e:
            mail_exception(exception=e)