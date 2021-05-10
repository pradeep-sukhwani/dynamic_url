import ast
from datetime import timedelta, datetime

from rest_framework import serializers
from core.models import URLDetail, URL


class URLDetailSerializer(serializers.ModelSerializer):
    # URL Detail serializer to serialize the data in a structured format
    raw_body = serializers.CharField(style={'base_template': 'textarea.html'}, allow_blank=True, allow_null=True)
    query_param = serializers.CharField(style={'base_template': 'textarea.html'}, allow_blank=True, allow_null=True)
    headers = serializers.CharField(style={'base_template': 'textarea.html'}, allow_blank=True, allow_null=True)

    class Meta:
        model = URLDetail
        fields = ('id', 'raw_body', 'query_param', 'headers')


class URLSerializer(serializers.ModelSerializer):
    # URL serializer to serialize the data in a structured format as well
    # as it is also used to create the URL & URLDetail instance
    url_details = URLDetailSerializer(many=True, allow_null=True, read_only=True)
    url_data = serializers.CharField(allow_null=True, allow_blank=True)
    headers = serializers.CharField(allow_null=True, allow_blank=True)
    minutes_seconds = serializers.SerializerMethodField('get_minutes_seconds')

    def get_minutes_seconds(self, instance):
        created_on_in_ist = instance.created_on
        created_on_ahead_one_hour = created_on_in_ist + timedelta(hours=1)
        current_datetime = datetime.now().astimezone()
        if created_on_in_ist <= created_on_ahead_one_hour and created_on_ahead_one_hour >= current_datetime:
            time_delta = created_on_ahead_one_hour - current_datetime
            total_seconds = time_delta.total_seconds()
            minutes = total_seconds / 60
            minutes = divmod(total_seconds, 60)
            return f'Expires in {round(minutes[0])} mins and {round(minutes[1], 2)} seconds'
        return 'Expired'
        diff = created_on - datetime.now()
        seconds = diff.seconds % (24 * 3600)
        hour = seconds // 3600
        if hour > 1:
            return 'Expired'
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        # return instance.created_on
        return f'Expires in {minutes} mins and {seconds} seconds'

    class Meta:
            model = URL
            fields = ('endpoint', 'created_on', 'hit_count', 'url_details', 'url_data', 'headers', 'minutes_seconds')

    def create(self, validated_data):
        # ast.literal_eval is used to convert string to dictionary
        url_data = ast.literal_eval(validated_data.pop('url_data'))
        headers = ast.literal_eval(validated_data.pop('headers'))
        obj = URL.objects.create(**validated_data)
        if url_data.get('query_params') or url_data.get('raw_body'):
            len_of_raw_body = len(url_data.get('raw_body'))
            for i in range(0, len_of_raw_body):
                raw_body = url_data.get('raw_body')[i]
                query_params = url_data.get('query_params')[i]
                url_detail = URLDetail.objects.create(query_param=raw_body or 'Nil', raw_body=query_params or 'Nil',
                                                      headers=headers)
                obj.url_details.add(url_detail)
        else:
            url_detail = URLDetail.objects.create(query_param='Nil', raw_body='Nil', headers=headers)
            obj.url_details.add(url_detail)
        return obj
