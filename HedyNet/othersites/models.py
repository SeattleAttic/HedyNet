from __future__ import unicode_literals

from django.db import models

class OtherSite(models.Model):
    """Links to other sites associated with the space."""

    EMBED_BELOW = "below"
    EMBED_RIGHT = "right"

    EMBED_POSITIONS = (
        (EMBED_BELOW, "below"),
        (EMBED_RIGHT, "right"),
    )
    
    # The choices for embed columns
    TOTAL_COLUMNS = 12
    COLUMN_CHOICES = zip(range(1,TOTAL_COLUMNS), range(1,TOTAL_COLUMNS))

    name = models.CharField(max_length = 30)
    order = models.PositiveSmallIntegerField(default = 100)
    display = models.BooleanField(default = True,
        help_text="Whether or not this site currently displays on the site.")
    slug = models.SlugField()
    link = models.URLField()
    
    description = models.TextField()
    embed_code = models.TextField(blank = True, null = True)
    
    embed_position = models.CharField(max_length=20, blank = True, null = True,
        choices = EMBED_POSITIONS)
    embed_columns = models.PositiveSmallIntegerField(blank = True, null = True,
        choices = COLUMN_CHOICES,
        help_text="For a side embed, the number of columns the embed takes up on a large page.")

    class Meta:
        ordering = ['order', 'name']

    def __unicode__(self):
        return self.name

    def _description_columns(self):
        if not self.embed_columns:
            return self.TOTAL_COLUMNS
        else:
            return self.TOTAL_COLUMNS - self.embed_columns
    description_columns = property(_description_columns)

    @models.permalink        
    def get_absolute_url(self):
        return ('othersite', (), {'slug': self.slug})
