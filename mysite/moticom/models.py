from django.db import models

class User(models.Model):
    user_name = models.CharField(max_length=50)
    email_adress = models.CharField(max_length=255)
    pub_date = models.DateTimeField(auto_now_add=True)
    pw_digest = models.CharField(max_length=130)
    def __str__(self):
        return self.user_name
    
class ControlMeasure(models.Model):
    cm_name = models.CharField(max_length=200)
    def __str__(self):
        return self.cm_name

class Genre(models.Model):
    genre_name = models.CharField(max_length=200)
    cm_id = models.ForeignKey(ControlMeasure, on_delete=models.CASCADE)
    def __str__(self):
        return self.genre_name
    
class Report(models.Model):
    report_text = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)
    def __str__(self):
        return self.report_text
    
class Like(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    report_id = models.ForeignKey(Report, on_delete=models.CASCADE)
    
class Bad(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    report_id = models.ForeignKey(Report, on_delete=models.CASCADE)
    