from django.core.serializers.python import Serializer


class CitySerializer(Serializer):
    def end_object( self, obj ):
        self._current['city_id'] = obj._get_pk_val()
        self.objects.append( self._current )