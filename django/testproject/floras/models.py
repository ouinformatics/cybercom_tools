# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class RtUnitConversionFactor(models.Model):
    reported_unit = models.CharField(unique=True, max_length=15)
    target_unit = models.CharField(unique=True, max_length=15)
    conversion_factor = models.DecimalField(null=True, max_digits=63, decimal_places=30, blank=True)
    delta = models.DecimalField(null=True, max_digits=63, decimal_places=30, blank=True)
    status_flag = models.CharField(max_length=1)
    ebatch = models.BigIntegerField(null=True, blank=True)
    remark = models.CharField(max_length=2000, blank=True)
    class Meta:
        db_table = u'rt_unit_conversion_factor'


class RtState(models.Model):
    state_code = models.CharField(unique=True, max_length=10)
    state_name = models.CharField(max_length=255, blank=True)
    status_flag = models.CharField(max_length=1)
    ebatch = models.BigIntegerField(null=True, blank=True)
    remark = models.CharField(max_length=2000, blank=True)
    class Meta:
        db_table = u'rt_state'

class DtLocationParameter(models.Model):
    commons_id = models.BigIntegerField(unique=True)
    loc_id = models.CharField(unique=True, max_length=20)
    param_id = models.DecimalField(unique=True, max_digits=30, decimal_places=0)
    param_name = models.CharField(max_length=255, blank=True)
    param_value = models.CharField(max_length=255, blank=True)
    param_unit = models.CharField(max_length=15, blank=True)
    remark = models.CharField(max_length=2000, blank=True)
    class Meta:
        db_table = u'dt_location_parameter'

class DtType(models.Model):
    type_id = models.CharField(unique=True, max_length=255)
    type_name = models.CharField(max_length=255, blank=True)
    product = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    resolution = models.CharField(max_length=255, blank=True)
    res_unit = models.CharField(max_length=50, blank=True)
    object_type = models.CharField(max_length=100, blank=True)
    object_data_opt1 = models.CharField(max_length=255, blank=True)
    object_data_opt1_unit = models.CharField(max_length=100, blank=True)
    class Meta:
        db_table = u'dt_type'

class RtUnit(models.Model):
    unit_code = models.CharField(unique=True, max_length=15)
    unit_desc = models.CharField(max_length=255, blank=True)
    unit_type = models.CharField(max_length=50, blank=True)
    status_flag = models.CharField(max_length=1)
    esri_xy = models.BigIntegerField(null=True, blank=True)
    esri_z = models.BigIntegerField(null=True, blank=True)
    ebatch = models.BigIntegerField(null=True, blank=True)
    remark = models.CharField(max_length=2000, blank=True)
    class Meta:
        db_table = u'rt_unit'

class RtResultType(models.Model):
    result_type_code = models.CharField(unique=True, max_length=10)
    result_type_desc = models.CharField(max_length=255, blank=True)
    status_flag = models.CharField(max_length=1)
    ebatch = models.BigIntegerField(null=True, blank=True)
    remark = models.CharField(max_length=2000, blank=True)
    class Meta:
        db_table = u'rt_result_type'

class DtPerson(models.Model):
    person_name = models.CharField(max_length=150)
    title = models.CharField(max_length=100, blank=True)
    address1 = models.CharField(max_length=40, blank=True)
    address2 = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=10, blank=True)
    postal_code = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    fax_number = models.CharField(max_length=30, blank=True)
    alt_phone_number = models.CharField(max_length=30, blank=True)
    email_address = models.CharField(max_length=100, blank=True)
    company_code = models.CharField(max_length=20, blank=True)
    certification_number = models.CharField(max_length=40, blank=True)
    people_id = models.DecimalField(unique=True, max_digits=30, decimal_places=0)
    class Meta:
        db_table = u'dt_person'

class RtLocationType(models.Model):
    location_type_code = models.CharField(unique=True, max_length=20)
    location_type_desc = models.CharField(max_length=255, blank=True)
    status_flag = models.CharField(max_length=1)
    ebatch = models.BigIntegerField(null=True, blank=True)
    remark = models.CharField(max_length=2000, blank=True)
    class Meta:
        db_table = u'rt_location_type'

class FloraData1(models.Model):
    ref_no = models.CharField(max_length=9, blank=True)
    pubtype = models.CharField(max_length=19, blank=True)
    proofedby = models.CharField(max_length=10, blank=True)
    sitename = models.CharField(max_length=72, blank=True)
    percexot = models.CharField(max_length=8, blank=True)
    state1 = models.CharField(max_length=6, blank=True)
    state2 = models.CharField(max_length=6, blank=True)
    state3 = models.CharField(max_length=6, blank=True)
    state4 = models.CharField(max_length=6, blank=True)
    state5 = models.CharField(max_length=6, blank=True)
    state6 = models.CharField(max_length=6, blank=True)
    state7 = models.CharField(max_length=6, blank=True)
    state8 = models.CharField(max_length=6, blank=True)
    year = models.CharField(max_length=4, blank=True)
    latitude_s_edge = models.CharField(max_length=15, blank=True)
    latitude_n_edge = models.CharField(max_length=15, blank=True)
    latitude_center = models.CharField(max_length=15, blank=True)
    longitude_e_edge = models.CharField(max_length=16, blank=True)
    longitude_w_edge = models.CharField(max_length=16, blank=True)
    longitude_center = models.CharField(max_length=16, blank=True)
    elevation_m = models.CharField(max_length=11, blank=True)
    min_elev_m = models.CharField(max_length=10, blank=True)
    max_elev_m = models.CharField(max_length=10, blank=True)
    area_hectares = models.CharField(max_length=13, blank=True)
    midlat = models.CharField(max_length=11, blank=True)
    midlon = models.CharField(max_length=12, blank=True)
    midelev = models.CharField(max_length=11, blank=True)
    parcels = models.CharField(max_length=7, blank=True)
    arbitrary = models.CharField(max_length=46, blank=True)
    habitat = models.CharField(max_length=37, blank=True)
    habitatisland = models.CharField(max_length=21, blank=True)
    physiographic = models.CharField(max_length=45, blank=True)
    physiographicisland = models.CharField(max_length=19, blank=True)
    political = models.CharField(max_length=29, blank=True)
    preservetype = models.CharField(max_length=24, blank=True)
    jurisdiction = models.CharField(max_length=25, blank=True)
    other_specify = models.CharField(max_length=18, blank=True)
    bot_effort = models.CharField(max_length=10, blank=True)
    no_families = models.CharField(max_length=11, blank=True)
    no_genera = models.CharField(max_length=9, blank=True)
    no_species = models.CharField(max_length=10, blank=True)
    no_tot_taxa = models.CharField(max_length=11, blank=True)
    no_indig_spp = models.CharField(max_length=12, blank=True)
    status = models.CharField(max_length=8, blank=True)
    shortstatus = models.CharField(max_length=11, blank=True)
    missing = models.CharField(max_length=117, blank=True)
    remarks = models.CharField(max_length=171, blank=True)
    updatesinref_no = models.CharField(max_length=40, blank=True)
    past_morerecentfloras = models.CharField(max_length=31, blank=True)
    mawannotations = models.CharField(max_length=42, blank=True)
    ceforexoticsanalysis = models.CharField(max_length=32, blank=True)
    class Meta:
        db_table = u'flora_data1'

class DtContributors(models.Model):
    commons_id = models.BigIntegerField(unique=True)
    contributor_id = models.DecimalField(unique=True, max_digits=30, decimal_places=0)
    project_title = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    remark = models.CharField(max_length=2000, blank=True)
    class Meta:
        db_table = u'dt_contributors'

class RtVarables(models.Model):
    var_id = models.CharField(unique=True, max_length=30)
    varable_name = models.CharField(max_length=255, blank=True)
    sort_order = models.BigIntegerField(null=True, blank=True)
    varable_type = models.CharField(max_length=30, blank=True)
    status_flag = models.CharField(max_length=1)
    var_short_name = models.CharField(max_length=30, blank=True)
    remark = models.CharField(max_length=2000, blank=True)
    class Meta:
        db_table = u'rt_varables'

class DtLocation(models.Model):
    commons_id = models.BigIntegerField(unique=True)
    loc_id = models.CharField(unique=True, max_length=60)
    loc_name = models.CharField(max_length=255, blank=True)
    data_provider = models.CharField(max_length=20, blank=True)
    loc_desc = models.CharField(max_length=1000, blank=True)
    loc_type = models.CharField(max_length=255, blank=True)
    loc_purpose = models.CharField(max_length=255, blank=True)
    loc_county = models.CharField(max_length=60, blank=True)
    loc_district = models.CharField(max_length=60, blank=True)
    loc_state = models.CharField(max_length=10, blank=True)
    lat = models.DecimalField(null=True, max_digits=60, decimal_places=30, blank=True)
    lon = models.DecimalField(null=True, max_digits=60, decimal_places=30, blank=True)
    northbounding = models.DecimalField(null=True, max_digits=60, decimal_places=30, blank=True)
    southbounding = models.DecimalField(null=True, max_digits=60, decimal_places=30, blank=True)
    eastbounding = models.DecimalField(null=True, max_digits=60, decimal_places=30, blank=True)
    westbounding = models.DecimalField(null=True, max_digits=60, decimal_places=30, blank=True)
    remark = models.CharField(max_length=2000, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    coord_system = models.CharField(max_length=255, blank=True)
    projection = models.CharField(max_length=255, blank=True)
    loc_order = models.DecimalField(null=True, max_digits=60, decimal_places=30, blank=True)
    base_loc_id = models.CharField(max_length=60, blank=True)
    class Meta:
        db_table = u'dt_location'

class Florainput(models.Model):
    ref_no = models.CharField(max_length=20, blank=True)
    pubtype = models.CharField(max_length=60, blank=True)
    prfdby = models.CharField(max_length=60, blank=True)
    sitename = models.CharField(max_length=200, blank=True)
    percexot = models.CharField(max_length=60, blank=True)
    state1 = models.CharField(max_length=7, blank=True)
    state2 = models.CharField(max_length=7, blank=True)
    state3 = models.CharField(max_length=7, blank=True)
    state4 = models.CharField(max_length=7, blank=True)
    state5 = models.CharField(max_length=7, blank=True)
    state6 = models.CharField(max_length=7, blank=True)
    state7 = models.CharField(max_length=7, blank=True)
    state8 = models.CharField(max_length=7, blank=True)
    year = models.CharField(max_length=15, blank=True)
    latsedge = models.CharField(max_length=30, blank=True)
    latnedge = models.CharField(max_length=30, blank=True)
    latcent = models.CharField(max_length=30, blank=True)
    loneedge = models.CharField(max_length=30, blank=True)
    lonwedge = models.CharField(max_length=30, blank=True)
    loncent = models.CharField(max_length=30, blank=True)
    elev = models.CharField(max_length=30, blank=True)
    minelev = models.CharField(max_length=30, blank=True)
    maxelev = models.CharField(max_length=30, blank=True)
    ahect = models.CharField(max_length=60, blank=True)
    midlat = models.CharField(max_length=60, blank=True)
    midlon = models.CharField(max_length=60, blank=True)
    midelev = models.CharField(max_length=60, blank=True)
    parcels = models.CharField(max_length=60, blank=True)
    arbitrary = models.CharField(max_length=60, blank=True)
    habitat = models.CharField(max_length=60, blank=True)
    habisland = models.CharField(max_length=60, blank=True)
    physiogr = models.CharField(max_length=60, blank=True)
    physiois = models.CharField(max_length=20, blank=True)
    political = models.CharField(max_length=60, blank=True)
    prestype = models.CharField(max_length=60, blank=True)
    juris = models.CharField(max_length=60, blank=True)
    other = models.CharField(max_length=60, blank=True)
    boteff = models.CharField(max_length=60, blank=True)
    families = models.CharField(max_length=60, blank=True)
    genera = models.CharField(max_length=60, blank=True)
    species = models.CharField(max_length=60, blank=True)
    tottaxa = models.CharField(max_length=60, blank=True)
    indigspp = models.CharField(max_length=60, blank=True)
    status = models.CharField(max_length=30, blank=True)
    shrtstat = models.CharField(max_length=30, blank=True)
    missing = models.CharField(max_length=117, blank=True)
    remarks = models.CharField(max_length=2000, blank=True)
    updatref = models.CharField(max_length=60, blank=True)
    pastfl = models.CharField(max_length=60, blank=True)
    anno = models.CharField(max_length=60, blank=True)
    ref_num = models.DecimalField(null=True, max_digits=60, decimal_places=30, blank=True)
    class Meta:
        db_table = u'florainput'

class RtMethod(models.Model):
    method_code = models.CharField(unique=True, max_length=20)
    method_name = models.CharField(max_length=255, blank=True)
    status_flag = models.CharField(max_length=1)
    base_method = models.CharField(max_length=20, blank=True)
    remark = models.CharField(max_length=2000, blank=True)
    method_desc = models.CharField(max_length=500, blank=True)
    class Meta:
        db_table = u'rt_method'

class DtDataCommons(models.Model):
    commons_id = models.BigIntegerField(unique=True)
    commons_code = models.CharField(max_length=20)
    data_provider = models.CharField(max_length=20, blank=True)
    commons_type = models.CharField(max_length=20, blank=True)
    program_code = models.CharField(max_length=20, blank=True)
    commons_name = models.CharField(max_length=60, blank=True)
    email_address = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=2000, blank=True)
    client = models.CharField(max_length=50, blank=True)
    project_manager = models.CharField(max_length=50, blank=True)
    start_date = models.DateField(null=True, blank=True)
    status_flag = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'dt_data_commons'

class DtEvent(models.Model):
    commons_id = models.BigIntegerField(unique=True)
    event_id = models.BigIntegerField(unique=True)
    cat_id = models.BigIntegerField()
    event_method = models.CharField(max_length=20, blank=True)
    event_date = models.DateField(null=True, blank=True)
    event_desc = models.CharField(max_length=500, blank=True)
    event_type = models.CharField(max_length=20, blank=True)
    loc_id = models.CharField(max_length=20, blank=True)
    custom_1 = models.CharField(max_length=255, blank=True)
    remark = models.CharField(max_length=2000, blank=True)
    event_name = models.CharField(max_length=255, blank=True)
    status_flag = models.CharField(max_length=1, blank=True)
    class Meta:
        db_table = u'dt_event'

class DtResult(models.Model):
    commons_id = models.BigIntegerField(unique=True)
    event_id = models.BigIntegerField(unique=True)
    var_id = models.CharField(unique=True, max_length=30)
    result_text = models.CharField(max_length=2000, blank=True)
    result_numeric = models.DecimalField(null=True, max_digits=60, decimal_places=30, blank=True)
    result_error = models.CharField(max_length=2000, blank=True)
    result_date = models.DateField(null=True, blank=True)
    stat_result = models.CharField(max_length=10, blank=True)
    result_order = models.DecimalField(null=True, max_digits=60, decimal_places=30, blank=True)
    result_unit = models.CharField(max_length=15, blank=True)
    remark = models.CharField(max_length=2000, blank=True)
    value_type = models.CharField(max_length=10, blank=True)
    stat_type = models.CharField(max_length=20, blank=True)
    validated = models.CharField(max_length=1, blank=True)
    class Meta:
        db_table = u'dt_result'

class DtCatalog(models.Model):
    commons_id = models.BigIntegerField(primary_key=True)
    cat_id = models.BigIntegerField(primary_key=True)
    cat_name = models.CharField(max_length=150, blank=True)
    data_provider = models.CharField(max_length=255, blank=True)
    cat_type = models.CharField(max_length=255, blank=True)
    loc_id = models.CharField(max_length=60, blank=True)
    source_id = models.DecimalField(null=True, max_digits=60, decimal_places=30, blank=True)
    cat_desc = models.CharField(max_length=255, blank=True)
    cat_method = models.CharField(max_length=40, blank=True)
    observe_date = models.DateField(null=True, blank=True)
    remark = models.CharField(max_length=2000, blank=True)
    year = models.DecimalField(null=True, max_digits=60, decimal_places=0, blank=True)
    custom_field_1 = models.CharField(max_length=255, blank=True)
    custom_field_2 = models.CharField(max_length=255, blank=True)
    status_flag = models.CharField(max_length=1, blank=True)
    status_data = models.CharField(max_length=20, blank=True)
    class Meta:
        db_table = u'dt_catalog'
    def _unicode_(self):
        return self.cat_name
