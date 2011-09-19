# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename model values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from django.forms import ModelForm

class RtStateForm(ModelForm):
    class Meta:
        model = RtState
class RtResultTypeForm(ModelForm):
    class Meta:
        model = models.RtResultType
class RtOrganizationTypeForm(ModelForm):
    class Meta:
         model = models.RtOrganizationType
class DtDataCommonsForm(ModelForm):
    class Meta:
        model = models.DtDataCommons
class RtVariablesForm(ModelForm):
    class Meta:
        model = models.RtVariables
class DtTypeForm(ModelForm):
    class Meta:
        model = models.DtType
class RtOrganizationForm(ModelForm):
    class Meta:
        model = models.RtOrganization
class DtPeopleForm(ModelForm):
    class Meta:
        model = models.DtPeople
class RtLocationTypeForm(ModelForm):
    class Meta:
        model = models.RtLocationType
class RtMethodForm(ModelForm):
    class Meta:
        model = models.RtMethod
class RtMethodParametersForm(ModelForm):
    class Meta:
        model = models.RtMethodParameters
class DtContributorsForm(ModelForm):
    class Meta:
        model = models.DtContributors
class DtLocationForm(ModelForm):
    class Meta:
        model = models.DtLocation
class DtLocationParameterForm(ModelForm):
    class Meta:
        model = models.DtLocationParameter
class DtCatalogForm(ModelForm):
    class Meta:
        model = models.DtCatalog
class DtEventForm(ModelForm):
    class Meta:
        model = models.DtEvent
class RtUnitForm(ModelForm):
    class Meta:
        model = models.RtUnit
class DtResultForm(ModelForm):
    class Meta:
        model = models.DtResult
