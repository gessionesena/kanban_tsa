from django.db import models
from django.contrib.auth.models import User


class Column(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order']



class Activity(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title
    



class Task(models.Model):
    title = models.CharField(max_length=150)
    discipline = models.ForeignKey('Discipline', on_delete=models.SET_NULL, null=True, blank=True)
    grade_level = models.ForeignKey('GradeLevel', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    column = models.ForeignKey(Column, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class GradeLevel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    

class Discipline(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



    
