from django.db import models
from django.utils import timezone

# Create your models here.

class Scales(models.Model):
    
    question_text= models.TextField()
    scale_name=models.CharField(max_length=200)
    
    def __str__(self):
        return self.question_text

class GenetUsers(models.Model):
    
    name=models.CharField(max_length=200, default="your_name_here")
    date=models.DateField(default=timezone.now())
    
class GenetUsersClassification(models.Model):

    user_id=models.AutoField(primary_key=True)
    user_classification=models.CharField(max_length=200)
    attention_check= models.CharField(max_length=200)
    question_1=models.TextField()
    answer_1=models.IntegerField()

    question_2=models.TextField()
    answer_2=models.IntegerField()

    question_3=models.TextField()
    answer_3=models.IntegerField()
    question_4=models.TextField()
    answer_4=models.IntegerField()
    question_5=models.TextField()
    answer_5=models.IntegerField()
    question_6=models.TextField()
    answer_6=models.IntegerField()
    question_7=models.TextField()
    answer_7=models.IntegerField()
    question_8=models.TextField()
    answer_8=models.IntegerField()
    question_9=models.TextField()
    answer_9=models.IntegerField()
    question_10=models.TextField()
    answer_10=models.IntegerField()
    question_11=models.TextField()
    answer_11=models.IntegerField()
    question_12=models.TextField()
    answer_12=models.IntegerField()
    question_13=models.TextField()
    answer_13=models.IntegerField()
    question_14=models.TextField()
    answer_14=models.IntegerField()
    question_15=models.TextField()
    answer_15=models.IntegerField()
    question_16=models.TextField()
    answer_16=models.IntegerField()
    question_17=models.TextField()
    answer_17=models.IntegerField()
    question_18=models.TextField()
    answer_18=models.IntegerField()
    question_19=models.TextField()
    answer_19=models.IntegerField()
    question_20=models.TextField()
    answer_20=models.IntegerField()
    question_21=models.TextField()
    answer_21=models.IntegerField()
    question_22=models.TextField()
    answer_22=models.IntegerField()
    question_23=models.TextField()
    answer_23=models.IntegerField()
    question_24=models.TextField()
    answer_24=models.IntegerField()
    question_25=models.TextField()
    answer_25=models.IntegerField()
    question_26=models.TextField()
    answer_26=models.IntegerField()
    question_27=models.TextField()
    answer_27=models.IntegerField()
    question_28=models.TextField()
    answer_28=models.IntegerField()
    question_29=models.TextField()
    answer_29=models.IntegerField()
    question_30=models.TextField()
    answer_30=models.IntegerField()
    question_31=models.TextField()
    answer_31=models.IntegerField()
    question_32=models.TextField()
    answer_32=models.IntegerField()
    question_33=models.TextField()
    answer_33=models.IntegerField()
    question_34=models.TextField()
    answer_34=models.IntegerField()
    question_35=models.TextField()
    answer_35=models.IntegerField()
    question_36=models.TextField()
    answer_36=models.IntegerField()
    question_37=models.TextField() 
    answer_37=models.IntegerField()

    def __str__(self):
        return str(self.user_id)

class Prototype2Questions(models.Model):

    question_text= models.TextField()
    question_type=models.CharField(max_length=200)
    
    def __str__(self):
        return self.question_text

class GenetUsers2(models.Model):

    user_id=models.AutoField(primary_key=True)
    user_classification=models.CharField(max_length=200)
    attention_check= models.CharField(max_length=200)
    
    question_1=models.TextField()
    answer_1=models.IntegerField()

    question_2=models.TextField()
    answer_2=models.IntegerField()

    question_3=models.TextField()
    answer_3=models.IntegerField()
    question_4=models.TextField()
    answer_4=models.IntegerField()
    question_5=models.TextField()
    answer_5=models.IntegerField()
    question_6=models.TextField()
    answer_6=models.IntegerField()
    question_7=models.TextField()
    answer_7=models.IntegerField()
    question_8=models.TextField()
    answer_8=models.IntegerField()
    question_9=models.TextField()
    answer_9=models.IntegerField()
    question_10=models.TextField()
    answer_10=models.IntegerField()
    question_11=models.TextField()
    answer_11=models.IntegerField()
    question_12=models.TextField()
    answer_12=models.IntegerField()
    question_13=models.TextField()
    answer_13=models.IntegerField()
    question_14=models.TextField()
    answer_14=models.IntegerField()
    question_15=models.TextField()
    answer_15=models.IntegerField()
    question_16=models.TextField()
    answer_16=models.IntegerField()
    question_17=models.TextField()
    answer_17=models.IntegerField()
    question_18=models.TextField()
    answer_18=models.IntegerField()
    question_19=models.TextField()
    answer_19=models.IntegerField()
    question_20=models.TextField()
    answer_20=models.IntegerField()
    question_21=models.TextField()
    answer_21=models.IntegerField()
    question_22=models.TextField()
    answer_22=models.IntegerField()
    question_23=models.TextField()
    answer_23=models.IntegerField()
    question_24=models.TextField()
    answer_24=models.IntegerField()
    question_25=models.TextField()
    answer_25=models.IntegerField()
    question_26=models.TextField()
    answer_26=models.IntegerField()
    question_27=models.TextField()
    answer_27=models.IntegerField()
    question_28=models.TextField()
    answer_28=models.IntegerField()
    question_29=models.TextField()
    answer_29=models.IntegerField()
    question_30=models.TextField()
    answer_30=models.IntegerField()
    question_31=models.TextField()
    answer_31=models.IntegerField()
    question_32=models.TextField()
    answer_32=models.IntegerField()
    question_33=models.TextField()
    answer_33=models.IntegerField()
    question_34=models.TextField()
    answer_34=models.IntegerField()
    def __str__(self):
        return str(self.user_id)
class Prototype3Questions(models.Model):
    
    question_text= models.TextField()
    
    def __str__(self):
        return self.question_text
    
class GenetUsers3(models.Model):

    user_id=models.AutoField(primary_key=True)
    user_classification=models.CharField(max_length=200)
    attention_check= models.CharField(max_length=200)
    question_1=models.TextField()
    answer_1=models.TextField()

    question_2=models.TextField()
    answer_2=models.TextField()

    question_3=models.TextField()
    answer_3=models.TextField()
    question_4=models.TextField()
    answer_4=models.TextField()
    question_5=models.TextField()
    answer_5=models.TextField()
    question_6=models.TextField()
    answer_6=models.TextField()
    question_7=models.TextField()
    answer_7=models.TextField()
    def __str__(self):
        return str(self.user_id)
