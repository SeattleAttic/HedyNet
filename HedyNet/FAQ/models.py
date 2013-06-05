from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models

class FAQSection(models.Model):
    
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    order = models.IntegerField(default=0)
    description = models.TextField(blank = True)
    
    class Meta:
        ordering = ['order', 'title']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('faqsection-detail', kwargs={'slug': self.slug})

class FAQItem(models.Model):
    
    question = models.CharField(max_length=255)
    slug = models.SlugField()    
    section = models.ForeignKey(FAQSection)
    order = models.IntegerField(default=0)
    summary_answer = models.TextField()
    full_answer = models.TextField(blank = True)

    # Automatic fields for date created and modified
    last_modified_on = models.DateTimeField(auto_now = True, editable = False,
        verbose_name = "date last modified")
    created_on = models.DateTimeField(auto_now_add = True, editable = False,
        verbose_name = "date created")

    class Meta:
        ordering = ['order', 'question']
    
    def __unicode__(self):
        return self.question
    
    def get_absolute_url(self):
        return reverse('faqitem-detail', kwargs={
            'section_slug': self.section.slug,
            'faq_slug': self.slug})
