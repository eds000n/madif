from django.db import models

# Create your models here.
class Instrument(models.Model):
	mnemonic = models.CharField(max_length=10)
	"""
		jicamarca ISR		jro
		jicamarca bistatic	jbr
		aqp FPI			aqf
		jicamarca FPI		jfp
		movil FPI		mfp
		jicamarca magnetometer	jmt
		JULIA			jul
	"""
	desc = models.CharField(max_length=200)
	def __unicode__(self):
		return self.desc
		#return self.mnemonic
	
class Experiment(models.Model):
	experimentTitle = models.CharField(max_length=300)
	optChar = models.CharField(max_length=1)
	"""
	Caracteres por experimento:
		drifts				D
		average drifts			d
		jicamarca oblique mode		O
		special drifts mode		S
		special averaged drifts mode	s
		jicamarca bistatic mode		B
		FPI-CARDINAL mode		c
		FPI-COMMON volume mode		v
		jicamarca magnetometer mode	M
		150km region drifts		K
		150km avg region drifts		k
		150km drifts-MST-ISR		m
		ESF				F
	"""
	def __unicode__(self):
		return self.experimentTitle

class ExpIns(models.Model):
	instrument = models.ForeignKey(Instrument)
	experiment = models.ForeignKey(Experiment)
	class Meta :
		unique_together = ("instrument","experiment")
	def __unicode__(self):
		return str(self.id)
	#	return self.experiment+self.instrument

class ExperimentData(models.Model):
	expins = models.ForeignKey(ExpIns)
	path = models.CharField(max_length=400)
	desc = models.CharField(max_length=200)
	permission = models.IntegerField()
	#optChar = models.CharField(max_length=1)
	fecha = models.DateField()
	def __unicode__(self):
		return self.desc
