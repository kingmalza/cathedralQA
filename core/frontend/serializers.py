from frontend.models import t_test, temp_main, temp_case, temp_keywords, temp_variables, temp_pers_keywords, \
    temp_test_keywords, temp_library, t_schedule, t_group, t_group_test, t_history, t_threads, t_tags, t_tags_route
from rest_framework import serializers
from django.contrib.auth.models import User


class t_testSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    #highlight = serializers.HyperlinkedIdentityField(view_name='request-highlight', format='html')
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = t_test
        fields = ('id', 'test_id', 'test_data', 'test_rst', 'owner')


class temp_mainSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    #highlight = serializers.HyperlinkedIdentityField(view_name='request-highlight', format='html')
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = temp_main
        fields = ('id', 'descr', 'notes', 'dt', 'owner')


class temp_caseSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    #highlight = serializers.HyperlinkedIdentityField(view_name='request-highlight', format='html')
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = temp_case
        fields = ('id', 'main_id', 'descr', 'owner')


class temp_keywordsSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    #highlight = serializers.HyperlinkedIdentityField(view_name='request-highlight', format='html')
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = temp_keywords
        fields = ('id', 'descr', 'human', 'personal', 'owner')


class temp_variablesSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    #highlight = serializers.HyperlinkedIdentityField(view_name='request-highlight', format='html')
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = temp_variables
        fields = ('id', 'main_id', 'v_key', 'v_val', 'owner')


class temp_pers_keywordsSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    #highlight = serializers.HyperlinkedIdentityField(view_name='request-highlight', format='html')
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = temp_pers_keywords
        fields = ('id', 'main_id', 'pers_id', 'standard_id', 'variable_val', 'owner')


class temp_test_keywordsSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    #highlight = serializers.HyperlinkedIdentityField(view_name='request-highlight', format='html')
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = temp_test_keywords
        fields = ('id', 'main_id', 'test_id', 'key_id', 'key_val', 'owner')


class temp_librarySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    #highlight = serializers.HyperlinkedIdentityField(view_name='request-highlight', format='html')
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = temp_library
        fields = ('id', 'main_id', 'l_type', 'l_val', 'owner')


class t_scheduleSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    #highlight = serializers.HyperlinkedIdentityField(view_name='request-highlight', format='html')
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = t_schedule
        fields = ('id', 'id_test', 'plan_data', 'exec_main', 'exec_every', 'exec_at', 'last_exec', 'active', 'owner')


class t_groupSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    #highlight = serializers.HyperlinkedIdentityField(view_name='request-highlight', format='html')
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = t_group
        fields = ('id', 'descr', 'g_prior', 'g_desc', 'user_id', 'active', 'owner')


class t_group_testSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    #highlight = serializers.HyperlinkedIdentityField(view_name='request-highlight', format='html')
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = t_group_test
        fields = ('id', 'id_grp', 'id_temp', 'temp_ord', 'owner')


class t_historySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    #highlight = serializers.HyperlinkedIdentityField(view_name='request-highlight', format='html')
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = t_history
        fields = ('id', 'test_main', 'exec_data', 'exec_status', 'xml_result', 'html_test', 'var_test', 'pid', 'user_id', 'group_id', \
                  'pass_num', 'fail_num', 'owner')


class t_threadsSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    #highlight = serializers.HyperlinkedIdentityField(view_name='request-highlight', format='html')
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = t_threads
        fields = ('id', 'id_test', 'thread_id', 'thread_main', 'thread_stag', 'thread_status', 'thread_startd', 'thread_stopd', 'owner')


class t_tagsSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    #highlight = serializers.HyperlinkedIdentityField(view_name='request-highlight', format='html')
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = t_tags
        fields = ('id', 'descr', 'tag_notes', 'owner')


class t_tags_routeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    #highlight = serializers.HyperlinkedIdentityField(view_name='request-highlight', format='html')
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = t_tags_route
        fields = ('id', 'main_id', 'tag_id', 'route_notes', 'owner')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # snippets = serializers.HyperlinkedRelatedField(queryset=ml_request.objects.all(), view_name='snippet-detail', many=True)

    class Meta:
        model = User
        fields = ('id', 'username')
