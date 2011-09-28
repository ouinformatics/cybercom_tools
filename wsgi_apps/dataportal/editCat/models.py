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
from django import forms
import datetime

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
    Status_Data_Choices = (('A','Active'),('I','Inactive'),)
    commons_id = models.AutoField(primary_key=True)
    commons_code = models.CharField(max_length=20)
    commons_type = models.CharField(max_length=20, null=True, blank=True)
    data_provider = models.CharField(max_length=20,null=True,blank=True)
    program_code = models.CharField(max_length=20, null=True, blank=True)
    commons_name = models.CharField(max_length=60, blank=True)
    commons_desc = models.CharField(max_length=2000, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    status_flag = models.CharField(max_length=1, blank=True, null=True, choices=Status_Data_Choices, default='A')
    def save(self):
        if self.commons_type=='': self.commons_type=None
        if self.data_provider=='': self.data_provider=None
        if self.program_code=='': self.program_code=None
        if self.commons_desc=='': self.commons_desc=None
        if self.status_flag=='': self.status_flag=None
        
        super(DtDataCommons,self).save()

    def __unicode__(self):
        return u'%s %s' % (self.commons_id, self.commons_name)
    class Meta:
        db_table = u'dt_data_commons'

class RtVariables(models.Model):
    var_id = models.CharField(max_length=30, primary_key=True)
    variable_name = models.CharField(max_length=255)
    sort_order = models.IntegerField(null=True,blank=True)
    variable_type = models.CharField(max_length=30,null=True,blank=True)
    status_flag = models.CharField(max_length=1)
    var_short_name = models.CharField(max_length=30,null=True,blank=True)
    remark = models.CharField(max_length=2000,null=True,blank=True)
    userid = models.CharField(max_length=20)
    def __unicode__(self):
        return u'(%s) -  %s' % (self.var_id, self.variable_name)
    class Meta:
        db_table = u'rt_variables'

class DtType(models.Model):
    type_id = models.CharField(max_length=40, primary_key=True)
    type_name = models.CharField(max_length=255)
    product = models.CharField(max_length=255,blank=True, null=True)
    description = models.CharField(max_length=255,blank=True, null=True)
    resolution = models.CharField(max_length=255,blank=True, null=True)
    res_unit = models.CharField(max_length=50,blank=True, null=True)
    object_type = models.CharField(max_length=100,blank=True, null=True)
    object_data_type1 = models.CharField(max_length=255,blank=True, null=True)
    object_data_opt1_unit = models.CharField(max_length=100,blank=True, null=True)
    userid = models.CharField(max_length=20)
    def save(self):
        if self.product=='': self.product=None
        if self.description=='': self.description=None
        if self.resolution=='': self.resolution=None
        if self.res_unit=='': self.res_unit=None
        if self.object_type=='': self.object_type=None
        if self.object_data_type1=='': self.object_data_type1=None
        if self.object_data_opt1_unit=='': self.object_data_opt1_unit=None
        super(DtType,self).save()
    def __unicode__(self):
        return u'%s %s' % (self.type_id, self.type_name)
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
    method_desc = models.CharField(max_length=500,null=True,blank=True)
    status_flag = models.CharField(max_length=1)
    remark = models.CharField(max_length=2000,null=True,blank=True)
    base_method = models.CharField(max_length=50,null=True,blank=True)
    userid = models.CharField(max_length=20)
    timestamp_created = models.DateTimeField(default= datetime.datetime.now())    
    def __unicode__(self):
        return u'%s %s' % (self.method_code, self.method_name)    
    class Meta:
        db_table = u'rt_method'

class RtMethodParameters(models.Model):
    method_code = models.ForeignKey(RtMethod, db_column='method_code')
    param_id = models.IntegerField()
    param_type = models.CharField(max_length=20)
    param_name = models.CharField(max_length=255)
    param_desc = models.CharField(max_length=500)
    param_value = models.CharField(max_length=255)
    method_id = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=20)
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
    loc_id = models.CharField(max_length=60,primary_key=True)
    commons_id = models.IntegerField()
    loc_name = models.CharField(max_length=255)
    data_provider = models.CharField(max_length=20,blank=True)
    loc_desc = models.CharField(max_length=1000,blank=True)
    loc_type = models.CharField(max_length=255,blank=True)#ForeignKey(RtLocationType, db_column='loc_type')
    loc_purpose = models.CharField(max_length=255,blank=True)
    loc_county = models.CharField(max_length=80,blank=True)
    loc_state = models.CharField(max_length=10,blank=True)
    lat = models.FloatField(blank=True)
    lon = models.FloatField(blank=True)
    northbounding = models.FloatField(blank=True)
    southbounding = models.FloatField(blank=True)
    eastbounding = models.FloatField(blank=True)
    westbounding = models.FloatField(blank=True)
    remark = models.CharField(max_length=2000,blank=True)
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)
    coord_system = models.CharField(max_length=255,blank=True)
    projection = models.CharField(max_length=255,blank=True)
    loc_order = models.IntegerField(blank=True)
    base_loc_id = models.CharField(max_length=60,blank=True)
    #django_id = models.AutoField(primary_key=True)
    unique_together = ("commons_id", "loc_id")
    def __unicode__(self):
        return u'%s %s' % (self.loc_id, self.loc_name)
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
class DtCatalog(models.Model):
    Status_Data_Choices = (('Data','Data'),('Application','Application'),)
    commons_id = models.IntegerField()#ForeignKey(DtDataCommons)
    cat_id = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=255)
    data_provider = models.CharField(max_length=255,blank=True)
    cat_type = models.ForeignKey(DtType, db_column='cat_type',blank=True,null=True)
    loc_id = models.ForeignKey(DtLocation,db_column='loc_id')
    source_id = models.IntegerField(blank=True)
    cat_desc = models.CharField(max_length=255,blank=True)#,widget=forms.Textarea)
    cat_method = models.ForeignKey(RtMethod, db_column='cat_method',blank=True,null=True)
    observed_date = models.DateTimeField(blank=True)
    remark = models.CharField(max_length=2000,blank=True)
    observed_year = models.IntegerField(blank=True)
    custom_field_1 = models.CharField(max_length=255,blank=True)
    custom_field_2 = models.CharField(max_length=255,blank=True)
    status_flag = models.CharField(max_length=1)
    status_data = models.CharField(max_length=20, choices=Status_Data_Choices, default = 'Data')
    userid = models.CharField(max_length=20)
    timestamp_created = models.DateTimeField(default= datetime.datetime.now())
    unique_together = ("commons_id", "cat_id")

    def save(self):
        if self.data_provider=='': self.data_provider=None
        if self.cat_type=='': self.cat_type=None
        if self.loc_id=='': self.loc_id=None
        if self.remark=='': self.remark=None
        if self.custom_field_1=='': self.custom_field_1=None
        if self.custom_field_2=='': self.custom_field_2=None
        if self.cat_desc=='': self.cat_desc=None
        super(DtCatalog,self).save()
    class Meta:
        db_table = u'dt_catalog'
class DtCatalog_defaults(DtCatalog):
    def __init__(self):
        DtCatalog.__init__(self)
        self["status_data"].choices = (('Data1','Data1'),('Application','Application'),)
class DtEvent(models.Model):
    commons_id = models.IntegerField()
    event_id = models.AutoField(primary_key=True)
    cat_id = models.IntegerField()
    event_name = models.CharField(max_length=255)
    event_desc = models.CharField(max_length=300,blank=True, null=True)
    event_method = models.ForeignKey(RtMethod, db_column='event_method',blank=True, null=True)
    event_date = models.DateTimeField(blank=True, null=True)
    event_type = models.ForeignKey(DtType, db_column='event_type',blank=True, null=True)
    loc_id = models.CharField(max_length=60,blank=True, null=True)
    custom_1 = models.CharField(max_length=300,blank=True, null=True)
    remark = models.CharField(max_length=2000,blank=True, null=True)
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
    result_id = models.AutoField(primary_key=True)
    commons_id = models.IntegerField()#.ForeignKey(DtEvent)
    event_id = models.IntegerField()
    var = models.ForeignKey(RtVariables)
    result_text = models.CharField(max_length=2000)
    result_numeric = models.FloatField(blank=True,null=True)
    result_error = models.CharField(max_length=300,blank=True,null=True)
    result_date = models.DateTimeField(blank=True,null=True)
    result_type = models.ForeignKey(RtResultType, db_column='result_type',blank=True,null=True)
    result_unit = models.ForeignKey(RtUnit, db_column='result_unit',blank=True,null=True)
    result_order = models.IntegerField(blank=True,null=True)
    stat_type = models.CharField(max_length=20,blank=True,null=True)
    stat_result = models.CharField(max_length=100,blank=True,null=True)
    validated = models.CharField(max_length=300,blank=True,null=True)
    remark = models.CharField(max_length=2000,blank=True,null=True)
    status_flag = models.CharField(max_length=1,default='A')
    validated_timestamp = models.DateTimeField(default= datetime.datetime.now())
    #userid = models.CharField(max_length=20)
    #timestamp_created = models.DateTimeField()
    unique_together = ("event_id", "var")
    class Meta:
        #primary_key = ('event_id','var')
        db_table =  u'dt_result'

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
    def __init__(self, *args, **kwargs):
        super(DtDataCommonsForm, self).__init__(*args, **kwargs)
        self.fields['status_flag'].label = "Display Flag"
        self.fields['start_date'].widget.attrs['readonly']= True
    class Meta:
        model = DtDataCommons
        fields = ('commons_name','commons_code','commons_desc','commons_type','data_provider','program_code','status_flag','start_date')
        widgets = {'commons_desc':forms.Textarea(attrs={'cols': 80, 'rows': 5}),
                    }

class RtVariablesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RtVariablesForm, self).__init__(*args, **kwargs)
        self.fields['var_id'].label = "Variable ID"
        self.fields['variable_name'].label = "Variable Name"
        self.fields['remark'].label = "Variable Description"
        self.fields['sort_order'].label = "Variable Order"
    class Meta:
        model = RtVariables
        fields = ('var_id', 'variable_name','remark','variable_type', 'sort_order',  'status_flag', 'userid')
        widgets = { 'remark': forms.Textarea(attrs={'cols': 75, 'rows': 5}),
                    #'commons_id':forms.HiddenInput(),
                    'status_flag':forms.HiddenInput(),
                    'userid':forms.HiddenInput(),
                    #'timestamp_created':forms.HiddenInput(),
                     }
class DtTypeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DtTypeForm, self).__init__(*args, **kwargs)
        self.fields['type_name'].label = "Type Name"
        self.fields['type_id'].label = "Type ID"
        self.fields['res_unit'].label = "Resolution Unit"
        self.fields['object_type'].label = "Data Definition"
        self.fields['object_data_type1'].label = "Optional Data Type"
        self.fields['object_data_opt1_unit'].label = "Optional Unit"
    class Meta:
        model = DtType
        fields = ('type_id', 'type_name', 'description','product', 'resolution', 'res_unit', 'object_type', 'object_data_type1', 'object_data_opt1_unit','userid')
        widgets = {'description': forms.Textarea(attrs={'cols': 75, 'rows': 5}),
                    #'commons_id':forms.HiddenInput(),
                    #'status_flag':forms.HiddenInput(),
                    'userid':forms.HiddenInput(),
                    #'timestamp_created':forms.HiddenInput(),
                     }

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
    def __init__(self, *args, **kwargs):
        super(RtMethodForm, self).__init__(*args, **kwargs)
        self.fields['method_desc'].label = "Method Description"
        self.fields['method_name'].label = "Method Name"
        self.fields['method_code'].label = "Method Code"
    class Meta:
        model = RtMethod
        fields = ('method_code', 'method_name', 'method_desc', 'status_flag', 'remark','userid')
        widgets = {'method_desc': forms.Textarea(attrs={'cols': 75, 'rows': 5}),
                    'status_flag':forms.HiddenInput(),
                    'userid':forms.HiddenInput(),
                     }
class RtMethodParametersForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RtMethodParametersForm, self).__init__(*args, **kwargs)
        #self.fields['param_id'].label = "Location Name"
        self.fields['param_name'].label = "Parameter Name"
        self.fields['param_desc'].label = "Parameter Description"
        self.fields['param_value'].label = "Parameter Value"
    class Meta:
        model = RtMethodParameters
        fields = ('method_code','param_name', 'param_desc', 'param_value', 'param_id', 'param_type','userid','method_id')
        widgets = {'param_desc': forms.Textarea(attrs={'cols': 75, 'rows': 5}),
                    'param_value': forms.Textarea(attrs={'cols': 75, 'rows': 5}),
                    'param_id':forms.HiddenInput(),
                    'userid':forms.HiddenInput(),
                     }
class DtContributorsForm(ModelForm):
    class Meta:
        model = DtContributors
class DtLocationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DtLocationForm, self).__init__(*args, **kwargs)
        self.fields['loc_name'].label = "Location Name"
        self.fields['loc_id'].label = "Location ID"
        self.fields['loc_desc'].label = "Description"
        self.fields['loc_type'].label = "Location Type"
        self.fields['loc_state'].label = "State"
        self.fields['loc_county'].label = "County"
        self.fields['coord_system'].label = "Coord. System"
        self.fields['lat'].label = "Latitude"
        self.fields['lon'].label = "Longitude"
        self.fields['loc_order'].label = "Location order"
        self.fields['loc_state'].label = "State"
        #self.fields['timestamp_created'].widget.attrs['readonly']= True
    class Meta:
        model = DtLocation
        fields = ('loc_id', 'commons_id', 'loc_name', 'loc_desc', 'lat', 'lon', 'northbounding', 'southbounding', 
                        'eastbounding', 'westbounding', 'data_provider','remark','loc_type', 'loc_county', 'loc_state','coord_system', 'projection', 'loc_order')
        widgets = {'loc_desc': forms.Textarea(attrs={'cols': 75, 'rows': 5}),
                    'commons_id':forms.HiddenInput(),
                    #'status_flag':forms.HiddenInput(),
                    #'userid':forms.HiddenInput(),
                    #'timestamp_created':forms.HiddenInput(),
                     }

class DtLocationParameterForm(ModelForm):
    class Meta:
        model = DtLocationParameter
class DtCatalogForm(ModelForm):
    class Meta:
        model = DtCatalog
class AjaxForm(ModelForm):
        def errors_as_json(self, strip_tags=False):
            error_summary = {}
            errors = {}
            for error in self.errors.iteritems():
                errors.update({error[0] : unicode(striptags(error[1]) \
                    if strip_tags else error[1])})
            error_summary.update({'errors' : errors })
            return error_summary
class DtCatalogForm_data(AjaxForm):#ModelForm):
    def __init__(self, *args, **kwargs):
        super(DtCatalogForm_data, self).__init__(*args, **kwargs)
        self.fields['status_data'].label = "Catalog Type"
        self.fields['loc_id'].label = "Location"
        self.fields['cat_type'].label = "Data Type"
        self.fields['cat_desc'].label = "Description"
        self.fields['cat_method'].label = "Catalog Method"
        self.fields['cat_name'].label = "Catalog Name"
        #self.fields['cat_method'].help_text = "this sucks Catalog Method"
        #print self.fields
        self.fields['timestamp_created'].widget.attrs['readonly']= True
        #self.fields['loc_id'].queryset = DtLocation.objects.filter(commons_id=5)
        cat_desc  = forms.CharField(widget=forms.Textarea)
        #loc_id = forms.ModelChoiceField(queryset=DtLocation.objects.filter(commons_id__in=[5,]))
        #timestamp_created  = forms.DateTimeField(widget=forms.DateTimeField(attrs={'readonly':'readonly'}))
        #timestamp_created = forms.DateTimeField(attrs={'readonly':'readonly'})
        #commons_id = form.CharField(widget=forms.Textarea)
        #loc_id = forms.CharField(max_length=60, queryset=DtLocation.objects.filter(commons_id = 14))
    class Meta:
        model = DtCatalog
        fields = ('commons_id','cat_name','status_data','cat_id','loc_id','cat_desc','cat_method', 'cat_type', 
                    'observed_date','observed_year', 'remark', 'custom_field_1', 
                    'custom_field_2', 'data_provider','status_flag', 'userid', 'timestamp_created')
        widgets = {'cat_desc': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
                    'remark': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
                    #'commons_id':forms.HiddenInput(),
                    'status_flag':forms.HiddenInput(),
                    'userid':forms.HiddenInput(),
                    'commons_id':forms.HiddenInput(),
                     }
class DtEventForm(ModelForm):#,commonsid=14,catid=860935):
    def __init__(self, *args, **kwargs):
        super(DtEventForm , self).__init__(*args, **kwargs)
        self.fields['timestamp_created'].widget.attrs['readonly']= True
        self.fields['commons_id'].widget.attrs['readonly']= True
        self.fields['cat_id'].widget.attrs['readonly']= True
        self.fields['cat_id'].label = "Catalog ID"
        self.fields['commons_id'].label = "Commons ID"
    # commons_id = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'readonly'}))#HiddenInput(), initial=14)
    # cat_id = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'readonly'}))#, initial=860935)
    class Meta:
        model = DtEvent
        fields = ('commons_id', 'event_id', 'cat_id', 'event_name', 'event_method','event_desc', 'event_type','event_date', 'remark', 'status_flag', 'userid', 'timestamp_created')
        widgets = {'event_desc': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
                    'remark': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
                    'status_flag':forms.HiddenInput(),
                    'commons_id':forms.HiddenInput(),
                    'cat_id':forms.HiddenInput(),
                    'userid':forms.HiddenInput(),
                    }
class DtEventForm1(ModelForm):
    class Meta:
        model = DtEvent
class RtUnitForm(ModelForm):
    class Meta:
        model = RtUnit
class DtResultForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DtResultForm , self).__init__(*args, **kwargs)
        self.fields['validated_timestamp'].widget.attrs['readonly']= True
        self.fields['validated_timestamp'].label ="Timestamp created"
        self.fields['var'].label ="Result Variable"
        self.fields['commons_id'].widget.attrs['readonly']= True
        self.fields['event_id'].widget.attrs['readonly']= True
        #self.fields['cat_id'].label = "Catalog ID"
        self.fields['commons_id'].label = "Commons ID"
    class Meta:
        model = DtResult
        fields = ('commons_id', 'event_id', 'var', 'result_text',  'result_order',  'remark', 'result_id', 'status_flag','validated_timestamp')
        widgets = { 'status_flag':forms.HiddenInput(),
                    'event_id':forms.HiddenInput(),
                    'commons_id':forms.HiddenInput(),
                    'userid':forms.HiddenInput(),
                    'result_text': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
                    }
