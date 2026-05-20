from django.db import models
from django.utils.text import slugify


class ProjectCategory(models.Model):
    """Categories for portfolio projects"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Project Category'
        verbose_name_plural = 'Project Categories'
    
    def __str__(self):
        return self.name


class Project(models.Model):
    """Portfolio project/case study"""
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True, related_name='projects')
    image = models.ImageField(upload_to='portfolio/%Y/%m/')
    
    # Short description for card
    description = models.CharField(max_length=200, help_text='Short description shown on card')
    
    # Full content sections
    about = models.TextField(help_text='About the project - full content')
    location = models.CharField(max_length=255)
    
    # Bullet points sections (stored as JSON or text with line breaks)
    services = models.TextField(help_text='Services offered (one per line)')
    software_tools = models.TextField(help_text='Software & Tools used (one per line)')
    key_elements = models.TextField(blank=True, null=True, help_text='Key Study Elements (one per line)')
    statistical_analysis = models.TextField(blank=True, null=True, help_text='Statistical & Technical Analysis (one per line)')
    
    # Display options
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
    
    def __str__(self):
        return self.name
    
    def get_services_list(self):
        """Return services as a list"""
        return [s.strip() for s in self.services.split('\n') if s.strip()]
    
    def get_tools_list(self):
        """Return tools as a list"""
        return [t.strip() for t in self.software_tools.split('\n') if t.strip()]
    
    def get_elements_list(self):
        """Return key elements as a list"""
        if self.key_elements:
            return [e.strip() for e in self.key_elements.split('\n') if e.strip()]
        return []
    
    def get_analysis_list(self):
        """Return statistical analysis as a list"""
        if self.statistical_analysis:
            return [a.strip() for a in self.statistical_analysis.split('\n') if a.strip()]
        return []
