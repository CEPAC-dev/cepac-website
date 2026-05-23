from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Project, ProjectCategory
import os
import re
from django.conf import settings
from pathlib import Path


def get_project_images(project_name):
    """Get all images for a project from static folder
    
    Handles naming patterns where:
    - Project name might have hyphens or spaces
    - Files might have numbers appended
    - Files are in local/ or global/ folders
    """
    images = []
    # Use main/static directory directly, not STATIC_ROOT
    base_path = Path(settings.BASE_DIR) / 'main' / 'static' / 'img' / 'portfolio'
    
    # Extract base name for matching (everything before first hyphen)
    # e.g., "Up View Mixed-Use Development" -> search for "Up View Mixed"
    base_name = project_name.split('-')[0].strip() if '-' in project_name else project_name
    
    # Search in both local and global folders
    for folder in ['local', 'global']:
        folder_path = base_path / folder
        if folder_path.exists():
            for file in sorted(os.listdir(folder_path)):
                # Case-insensitive matching
                file_lower = file.lower()
                base_lower = base_name.lower()
                
                # Match if filename starts with base name (allowing numbers after the name)
                # e.g., "Up View Mixed1-1.png" matches "Up View Mixed"
                if file_lower.startswith(base_lower):
                    images.append({
                        'filename': file,
                        'path': f'/static/img/portfolio/{folder}/{file}',
                        'url': f'/static/img/portfolio/{folder}/{file}',
                        'is_main': re.search(r'-1\.\w+$', file)  # Main image if it ends with -1.ext
                    })
    
    return sorted(images, key=lambda x: (not x['is_main'], x['filename']))


def get_main_project_image(project_name):
    """Get the main image (-1) for a project"""
    images = get_project_images(project_name)
    for img in images:
        if img['is_main']:
            return img['url']
    # Fallback to first image
    return images[0]['url'] if images else None


def projects_list(request):
    """Display all projects as cards"""
    projects = Project.objects.exclude(category__slug='research').all()
    categories = ProjectCategory.objects.exclude(slug='research').all()
    
    # Filter by category if provided
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(ProjectCategory, slug=category_slug)
        projects = projects.filter(category=category)
    
    # Add main image path to each project (AFTER filtering)
    for project in projects:
        project.main_image = get_main_project_image(project.name)
    
    context = {
        'projects': projects,
        'categories': categories,
        'selected_category': category_slug,
    }
    return render(request, 'portfolio/projects_list.html', context)


def project_detail(request, slug):
    """Display full project details"""
    project = get_object_or_404(Project, slug=slug)
    
    # Get all images for this project
    project.all_images = get_project_images(project.name)
    project.main_image = get_main_project_image(project.name)
    
    # Get related projects from same category
    related_projects = Project.objects.filter(
        category=project.category
    ).exclude(id=project.id)[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'portfolio/project_detail.html', context)
