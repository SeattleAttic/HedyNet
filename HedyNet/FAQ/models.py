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
    answer = models.TextField()
    # TODO: add date created & date modified
    
    class Meta:
        ordering = ['order', 'question']
    
    def __unicode__(self):
        return self.question
    
    def get_absolute_url(self):
        return reverse('faqitem-detail', kwargs={
            'section_slug': self.section.slug,
            'faq_slug': self.slug})
