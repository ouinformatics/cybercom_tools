# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from django.forms import ModelForm
from cybercom.data.catalog import datalayer

class RtState(models.Model):
    state_code = models.CharField(max_length=10, primary_key=True)
    state_name = models.CharField(max_length=255)
    status_flag = models.CharField(max_length=1)
    remark = models.CharField(max_length=2000)
    class Meta:
        db_table = u'rt_state'

class RtResultType(models.Model):
    result_type_code = models.CharField(max_length=20, primary_key=True)
    result_type_desc = models.CharField(max_length=255)
    status_flag = models.CharField(max_length=1)
    remark = models.CharField(max_length=2000)
    class Meta:
        db_table = u'rt_result_type'

class RtOrganizationType(models.Model):
    org_type = models.CharField(max_length=20, primary_key=True)
    org_type_desc = models.CharField(max_length=255)
    status_flag = models.CharField(max_length=1)
    remark = models.CharField(max_length=2000)
    class Meta:
        db_table = u'rt_organization_type'

class DtDataCommons(models.Model):
    commons_id = models.IntegerField(primary_key=True)
    commons_code = models.CharField(max_length=20)
    commons_type = models.CharField(max_length=20)
    data_provider = models.CharField(max_length=20)
    program_code = models.CharField(max_length=20)
    commons_name = models.CharField(max_length=60)
    commons_desc = models.CharField(max_length=2000)
    start_date = models.DateTimeField()
    status_flag = models.CharField(max_length=1)
    def __unicode__(self):
        return u'%s %s' % (self.commons_code, self.commons_name)
    class Meta:
        db_table = u'dt_data_commons'

class RtVariables(models.Model):
    var_id = models.CharField(max_length=30, primary_key=True)
    variable_name = models.CharField(max_length=255)
    sort_order = models.IntegerField()
    variable_type = models.CharField(max_length=30)
    status_flag = models.CharField(max_length=1)
    var_short_name = models.CharField(max_length=30)
    remark = models.CharField(max_length=2000)
    class Meta:
        db_table = u'rt_variables'

class DtType(models.Model):
    type_id = models.CharField(max_length=40, primary_key=True)
    type_name = models.CharField(max_length=255)
    product = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    resolution = models.CharField(max_length=255)
    res_unit = models.CharField(max_length=50)
    object_type = models.CharField(max_length=100)
    object_data_type1 = models.CharField(max_length=255)
    object_data_opt1_unit = models.CharField(max_length=100)
    class Meta:
        db_table = u'dt_type'

class SchemaVersion(models.Model):
    key = models.CharField(max_length=255, primary_key=True)
    timestamp = models.DateTimeField()
    extra = models.CharField(max_length=255)
    sfile = models.CharField(max_length=255)
    class Meta:
        db_table = u'schema_version'

class RtOrganization(models.Model):
    org_code = models.CharField(max_length=20, primary_key=True)
    org_name = models.CharField(max_length=255)
    org_type = models.ForeignKey(RtOrganizationType, db_column='org_type')
    status_flag = models.CharField(max_length=1)
    remark = models.CharField(max_length=2000)
    class Meta:
        db_table = u'rt_organization'

class DtPeople(models.Model):
    people_id = models.IntegerField(primary_key=True)
    person_name = models.CharField(max_length=255)
    title = models.CharField(max_length=100)
    address1 = models.CharField(max_length=80)
    address2 = models.CharField(max_length=80)
    city = models.CharField(max_length=40)
    state = models.ForeignKey(RtState, db_column='state')
    postal_code = models.CharField(max_length=15)
    country = models.CharField(max_length=80)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    org_code = models.ForeignKey(RtOrganization, db_column='org_code')
    class Meta:
        db_table = u'dt_people'

class RtLocationType(models.Model):
    location_type_code = models.CharField(max_length=50, primary_key=True)
    location_type_desc = models.CharField(max_length=255)
    status_flag = models.CharField(max_length=1)
    remark = models.CharField(max_length=2000)
    class Meta:
        db_table = u'rt_location_type'

class RtMethod(models.Model):
    method_code = models.CharField(max_length=50, primary_key=True)
    method_name = models.CharField(max_length=255)
    method_desc = models.CharField(max_length=500)
    status_flag = models.CharField(max_length=1)
    remark = models.CharField(max_length=2000)
    base_method = models.CharField(max_length=50)
    class Meta:
        db_table = u'rt_method'

class RtMethodParameters(models.Model):
    method_code = models.ForeignKey(RtMethod, db_column='method_code')
    param_id = models.IntegerField()
    param_type = models.CharField(max_length=20)
    param_name = models.CharField(max_length=255)
    param_desc = models.CharField(max_length=500)
    param_value = models.CharField(max_length=255)
    class Meta:
        db_table = u'rt_method_parameters'

class DtContributors(models.Model):
    commons = models.ForeignKey(DtDataCommons)
    people = models.ForeignKey(DtPeople)
    project_title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    remark = models.CharField(max_length=2000)
    class Meta:
        db_table = u'dt_contributors'

class DtLocation(models.Model):
    loc_id = models.CharField(max_length=60)
    commons_id = models.IntegerField()
    loc_name = models.CharField(max_length=255)
    data_provider = models.CharField(max_length=20)
    loc_desc = models.CharField(max_length=1000)
    loc_type = models.ForeignKey(RtLocationType, db_column='loc_type')
    loc_purpose = models.CharField(max_length=255)
    loc_county = models.CharField(max_length=80)
    loc_state = models.CharField(max_length=10)
    lat = models.FloatField()
    lon = models.FloatField()
    northbounding = models.FloatField()
    southbounding = models.FloatField()
    eastbounding = models.FloatField()
    westbounding = models.FloatField()
    remark = models.CharField(max_length=2000)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    coord_system = models.CharField(max_length=255)
    projection = models.CharField(max_length=255)
    loc_order = models.IntegerField()
    base_loc_id = models.CharField(max_length=60)
    class Meta:
        db_table = u'dt_location'

class DtLocationParameter(models.Model):
    commons = models.ForeignKey(DtLocation)
    loc_id = models.CharField(max_length=60)
    param_id = models.IntegerField()
    param_name = models.CharField(max_length=255)
    param_value = models.CharField(max_length=255)
    param_unit = models.CharField(max_length=15)
    remark = models.CharField(max_length=2000)
    class Meta:
        db_table = u'dt_location_parameter'
def getChoices(table,pk,descCol, where=None):
    md= datalayer.Metadata()
    cur=md.Search(table,where=where)
    l=[]
    desc=''
    first = True
    for row in cur:
        for col in descCol:
            if not first:
                desc =desc + ' - '
            desc=desc + str(row[col])
            first=False
        l.append((row[pk],desc ))
        desc=''
        first=True
    return l #tuple(l)
class DtCatalog(models.Model):
    Status_Data_Choices = (('Data','Data'),('Application','Application'),)
    #commons_choice= ((100,'Data'),(300,'Application'),)
    #commons_choice=getChoices('dt_data_commons','commons_id',['commons_code'])
    #type_choice = getChoices('dt_type','type_id',['type_name','product'],where='type_id in (select distinct cat_type from dt_catalog )')
    #method_choices = getChoices('rt_method','method_code',['method_code','method_name'])
    #loc_choices = getChoices('dt_location','loc_id',['loc_name'],where='loc_id is not null order by commons_id,loc_order')
    commons = models.ForeignKey(DtDataCommons)#,choices = commons_choice)
    cat_id = models.AutoField(primary_key=True)#IntegerField(primary_key=True)
    cat_name = models.CharField(max_length=255)
    data_provider = models.CharField(max_length=255,blank=True)
    cat_type = models.ForeignKey(DtType, db_column='cat_type')#,choices = type_choice)
    loc_id = models.CharField(max_length=60)#,choices = loc_choices)
    source_id = models.IntegerField(blank=True)
    cat_desc = models.CharField(max_length=255)
    cat_method = models.ForeignKey(RtMethod, db_column='cat_method')#,choices = method_choices)
    observed_date = models.DateTimeField()
    remark = models.CharField(max_length=2000)
    observed_year = models.IntegerField()
    custom_field_1 = models.CharField(max_length=255)
    custom_field_2 = models.CharField(max_length=255)
    status_flag = models.CharField(max_length=1)
    status_data = models.CharField(max_length=20, choices=Status_Data_Choices)
    userid = models.CharField(max_length=20)
    timestamp_created = models.DateTimeField()
    unique_together = ("commons", "cat_id")
    class Meta:
        db_table = u'dt_catalog'
class DtCatalog_defaults(DtCatalog):
    def __init__(self):
        DtCatalog.__init__(self)
        self["status_data"].choices = (('Data1','Data1'),('Application','Application'),)
class DtEvent(models.Model):
    commons = models.ForeignKey(DtCatalog)
    event_id = models.IntegerField()
    cat_id = models.IntegerField()
    event_name = models.CharField(max_length=255)
    event_desc = models.CharField(max_length=300)
    event_method = models.ForeignKey(RtMethod, db_column='event_method')
    event_date = models.DateTimeField()
    event_type = models.ForeignKey(DtType, db_column='event_type')
    loc_id = models.CharField(max_length=60)
    custom_1 = models.CharField(max_length=300)
    remark = models.CharField(max_length=2000)
    status_flag = models.CharField(max_length=1)
    userid = models.CharField(max_length=20)
    timestamp_created = models.DateTimeField()
    class Meta:
        db_table = u'dt_event'

class Test1(models.Model):
    commons_id = models.IntegerField()
    cat_id = models.IntegerField()
    cat_name = models.CharField(max_length=255)
    data_provider = models.CharField(max_length=255)
    cat_type = models.CharField(max_length=40)
    loc_id = models.CharField(max_length=60)
    source_id = models.IntegerField()
    cat_desc = models.CharField(max_length=255)
    cat_method = models.CharField(max_length=50)
    observed_date = models.DateTimeField()
    remark = models.CharField(max_length=2000)
    observed_year = models.IntegerField()
    custom_field_1 = models.CharField(max_length=255)
    custom_field_2 = models.CharField(max_length=255)
    status_flag = models.CharField(max_length=1)
    status_data = models.CharField(max_length=20)
    userid = models.CharField(max_length=20)
    timestamp_created = models.DateTimeField()
    class Meta:
        db_table = u'test1'

class RtUnit(models.Model):
    unit_code = models.CharField(max_length=15, primary_key=True)
    unit_desc = models.CharField(max_length=255)
    unit_type = models.CharField(max_length=15)
    status_flag = models.CharField(max_length=1)
    remark = models.CharField(max_length=2000)
    class Meta:
        db_table = u'rt_unit'

class DtResult(models.Model):
    commons = models.ForeignKey(DtEvent)
    event_id = models.IntegerField()
    var = models.ForeignKey(RtVariables)
    result_text = models.CharField(max_length=2000)
    result_numeric = models.FloatField()
    result_error = models.CharField(max_length=300)
    result_date = models.DateTimeField()
    result_type = models.ForeignKey(RtResultType, db_column='result_type')
    result_unit = models.ForeignKey(RtUnit, db_column='result_unit')
    result_order = models.IntegerField()
    stat_type = models.CharField(max_length=20)
    stat_result = models.CharField(max_length=100)
    validated = models.CharField(max_length=300)
    remark = models.CharField(max_length=2000)
    status_flag = models.CharField(max_length=1)
    validated_timestamp = models.DateTimeField()
    class Meta:
        db_table = u'dt_result'

class CatalogMetadata(models.Model):
    cat_id = models.IntegerField()
    cat_name = models.CharField(max_length=255)
    cat_method = models.CharField(max_length=50)
    event_id = models.IntegerField()
    event_method = models.CharField(max_length=50)
    var_id = models.CharField(max_length=30)
    result_text = models.CharField(max_length=2000)
    class Meta:
        db_table = u'catalog_metadata'

class LocCatalogMeta(models.Model):
    cat_id = models.IntegerField()
    cat_name = models.CharField(max_length=255)
    cat_method = models.CharField(max_length=50)
    event_id = models.IntegerField()
    event_method = models.CharField(max_length=50)
    var_id = models.CharField(max_length=30)
    result_text = models.CharField(max_length=2000)
    loc_id = models.CharField(max_length=60)
    class Meta:
        db_table = u'loc_catalog_meta'

class RtStateForm(ModelForm):
    class Meta:
        model = RtState
class RtResultTypeForm(ModelForm):
    class Meta:
        model = RtResultType
class RtOrganizationTypeForm(ModelForm):
    class Meta:
         model = RtOrganizationType
class DtDataCommonsForm(ModelForm):
    class Meta:
        model = DtDataCommons
class RtVariablesForm(ModelForm):
    class Meta:
        model = RtVariables
class DtTypeForm(ModelForm):
    class Meta:
        model = DtType
class RtOrganizationForm(ModelForm):
    class Meta:
        model = RtOrganization
class DtPeopleForm(ModelForm):
    class Meta:
        model = DtPeople
class RtLocationTypeForm(ModelForm):
    class Meta:
        model = RtLocationType
class RtMethodForm(ModelForm):
    class Meta:
        model = RtMethod
class RtMethodParametersForm(ModelForm):
    class Meta:
        model = RtMethodParameters
class DtContributorsForm(ModelForm):
    class Meta:
        model = DtContributors
class DtLocationForm(ModelForm):
    class Meta:
        model = DtLocation
class DtLocationParameterForm(ModelForm):
    class Meta:
        model = DtLocationParameter
class DtCatalogForm(ModelForm):
    class Meta:
        model = DtCatalog
class DtCatalogForm_data(ModelForm):
    class Meta:
        model = DtCatalog
        fields = ('commons', 'cat_name', 'data_provider', 'cat_type', 'loc_id', 'cat_desc', 'cat_method', 'observed_date','observed_year', 'remark', 'custom_field_1', 'custom_field_2', 'status_flag', 'status_data', 'userid', 'timestamp_created')
class DtEventForm(ModelForm):
    class Meta:
        model = DtEvent
class RtUnitForm(ModelForm):
    class Meta:
        model = RtUnit
class DtResultForm(ModelForm):
    class Meta:
        model = DtResult
