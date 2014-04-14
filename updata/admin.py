from django.contrib import admin
from updata.models import Experiment, Instrument, ExperimentData, ExpIns
# Register your models here.
#admin.site.register(Experiment)
#admin.site.register(Instrument)
#admin.site.register(ExpIns)
admin.site.register(ExperimentData)

class InstrumentAdmin(admin.ModelAdmin):
	#fieldsets = [
	#	(None, {'fields': ['id']}),
	#	('Instrumento',{'fields':['instrument'],'classes':['collapse']}),
	#	('Mnemonic', {'fields':['mnemonic']}),
	#]
	list_display = ('id','desc','mnemonic')
	search_fields = ['desc']

class ExperimentAdmin(admin.ModelAdmin):
	list_display = ('id', 'experimentTitle','optChar')
	search_fields = ['experimentTitle']

class ExpInsAdmin(admin.ModelAdmin):
	list_display = ('id','instrument','experiment')
	#list_display = ('id','instrument','instrument_id','experiment')
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(ExpIns, ExpInsAdmin)
