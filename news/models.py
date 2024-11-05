from django.db import models

class News(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to='news_pdfs/')
    date_published = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

# New Model for CSV Uploads
class InflationData(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inflation Data uploaded on {self.uploaded_at}"
    

class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)
    sentiment_label = models.CharField(max_length=10, null=True, blank=True)
    positive_score = models.FloatField(null=True, blank=True)
    neutral_score = models.FloatField(null=True, blank=True)
    negative_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title
    


class Comment(models.Model):
    article = models.ForeignKey(NewsArticle, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment on {self.article.title} - {self.text[:20]}'    