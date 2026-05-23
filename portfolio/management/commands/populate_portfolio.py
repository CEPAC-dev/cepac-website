from django.core.management.base import BaseCommand
from portfolio.models import ProjectCategory, Project
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Populate portfolio with sample Traffic Impact Study projects'

    def handle(self, *args, **options):
        # Create categories
        local_category, _ = ProjectCategory.objects.get_or_create(
            name='Local Projects',
            defaults={'slug': 'local-projects', 'description': 'Traffic Impact Studies in Egypt'}
        )
        global_category, _ = ProjectCategory.objects.get_or_create(
            name='Global Projects',
            defaults={'slug': 'global-projects', 'description': 'Traffic Impact Studies Worldwide'}
        )
        research_category, _ = ProjectCategory.objects.get_or_create(
            name='Research',
            defaults={'slug': 'research', 'description': 'Transportation Research & Development'}
        )

        self.stdout.write(self.style.SUCCESS('✓ Categories created'))

        # Sample projects data
        projects_data = [
            {
                'name': 'Up View Mixed-Use Development',
                'category': local_category,
                'location': '6th of October City, Giza, Egypt',
                'description': 'Comprehensive Traffic Impact Study for a high-rise mixed-use development.',
                'about': 'CEPAC conducted a comprehensive Traffic Impact Study for the Up View Mixed-Use Development located in 6th of October City, Giza. The project includes residential, commercial, administrative, and serviced apartment components across high-rise and low-rise buildings. The study covered traffic surveys, parking assessment, trip generation analysis, internal circulation evaluation, and future traffic forecasting using advanced transportation modeling and simulation tools to ensure efficient traffic operations and network performance.',
                'services': '''Traffic Impact Study (TIS)
Traffic Surveys & Data Collection
Parking Demand Assessment
Internal Circulation Analysis
Junction & Access Evaluation
Traffic Simulation Modeling
Future Traffic Forecasting
Transportation Network Assessment''',
                'software_tools': '''PTV VISSIM
PTV VISUM
TURN-AUTO
MATLAB
Google Earth''',
                'key_elements': '''Existing and future traffic condition assessments
Peak hour traffic analysis
Vehicle classification surveys
Parking demand and supply evaluation
Road network coding and traffic assignment
VISSIM microsimulation
Future year traffic analysis''',
            },
            {
                'name': 'SKY RIDGE EXECUTIVES',
                'category': local_category,
                'location': 'Sheraton Area – East Cairo, Egypt',
                'description': 'Traffic Impact Study for a premium executive residential complex.',
                'about': 'CEPAC conducted a comprehensive Traffic Impact Study (TIS) for the SKY RIDGE EXECUTIVES Project located in the Sheraton area, East Cairo. The study evaluated the impact of the development on the surrounding transportation network through detailed traffic analysis, parking assessment, trip generation and distribution, and operational evaluation of nearby intersections and corridors.',
                'services': '''Traffic Impact Study (TIS)
Traffic Surveys & Traffic Counts
Parking Demand Assessment
Trip Generation & Distribution
Internal Circulation Analysis
Access & Ramp Evaluation
Intersection Capacity Assessment
Traffic Forecasting
Transportation Network Evaluation
Microsimulation Modeling
Traffic Improvement Recommendations''',
                'software_tools': '''PTV VISSIM
PTV VISUM
Google Earth
Traffic Modeling & Simulation Tools''',
                'key_elements': '''Existing and future traffic condition assessments
Peak hour traffic analysis
Vehicle classification surveys
Evaluation of project gates and ramps
Parking demand and supply assessment
Road network coding and traffic assignment
VISSIM microsimulation for surrounding intersections
Future year operational analysis for 2026 and 2030
Engineering mitigation and traffic improvement proposals''',
            },
            {
                'name': 'Egypt Trip Generation Manual Development',
                'category': research_category,
                'location': 'Egypt',
                'description': 'Development of localized trip generation rates based on Egyptian travel behavior.',
                'about': 'CEPAC developed a comprehensive Egyptian Trip Generation Manual aimed at establishing localized trip generation rates based on Egyptian travel behavior and land-use characteristics. The manual serves as a unified reference for government authorities, developers, consultants, and transportation planners involved in Traffic Impact Studies (TIS) and urban mobility planning across Egypt.',
                'services': '''Transportation Research & Development
Trip Generation Analysis
Traffic Data Collection
Statistical Transportation Analysis
Peak Hour Analysis
Transportation Planning
Traffic Engineering Research
Benchmarking & Comparative Analysis
Urban Mobility Assessment
Traffic Impact Study Support''',
                'key_elements': '''Local trip generation rate development
Egyptian travel behavior analysis
Statistical calibration and validation
Field traffic surveys
Vehicle classification analysis
Peak hour determination
Modal split analysis
Occupancy analysis
Regression modeling and benchmarking
Comparison between local and international trip generation rates''',
                'software_tools': '''MATLAB
Python Statistical Analysis
ArcGIS
Excel/Statistical Packages
Transportation Modeling Tools''',
                'statistical_analysis': '''Average Rate Calculations
Standard Deviation
Range Analysis
Coefficient of Variation
Regression Equations
Coefficient of Determination (R²)''',
            },
            {
                'name': 'Kuwait Swimming Federation Headquarters',
                'category': global_category,
                'location': 'Sabah Al-Salem – Mubarak Al-Kabeer Governorate – Kuwait',
                'description': 'Comprehensive Traffic Impact Study for a world-class aquatic sports facility.',
                'about': 'CEPAC conducted a comprehensive Traffic Impact Study (TIS) for the proposed Kuwait Swimming Federation Headquarters located in Sabah Al-Salem, Mubarak Al-Kabeer Governorate, Kuwait. The study evaluated the transportation impact of the development on the surrounding road network, including traffic generation, parking demand, site accessibility, internal circulation, and future traffic operations under multiple forecast scenarios up to 2040.',
                'services': '''Traffic Impact Study (TIS)
Transportation Modeling
Traffic Surveys & Traffic Counts
Parking Demand & Supply Assessment
Internal Circulation Analysis
Access & Egress Evaluation
Junction Capacity Assessment
Future Traffic Forecasting
VISUM Transportation Modeling
VISSIM Microsimulation Analysis
Mitigation & Improvement Strategies
Event Traffic Management Assessment''',
                'software_tools': '''PTV VISSIM
PTV VISUM
Traffic Microsimulation Tools
Transportation Forecasting Models''',
                'key_elements': '''Existing traffic condition assessment
Peak hour traffic analysis
Parking adequacy evaluation
Event-based traffic demand assessment
Internal traffic circulation evaluation
Public transport accessibility analysis
Traffic forecasting for 2030 & 2040
Future "With Project" and "Without Project" scenarios
Intersection operational analysis using VISSIM
Traffic mitigation and lane improvement proposals
External parking management strategies for major events''',
            },
            {
                'name': 'Jleeb Al-Shuyoukh Commercial Development',
                'category': global_category,
                'location': 'Jleeb Al-Shuyoukh – Al Farwaniyah Governorate – Kuwait',
                'description': 'Traffic Impact Study for a multi-storey commercial development.',
                'about': 'CEPAC conducted a comprehensive Traffic Impact Study (TIS) for the proposed commercial development located at Plots 7 & 8 in Jleeb Al-Shuyoukh, Al Farwaniyah Governorate, Kuwait. The study evaluated the project\'s impact on the surrounding transportation network through detailed traffic analysis, parking assessment, trip generation, transportation modeling, and future operational evaluation up to the year 2040.',
                'services': '''Traffic Impact Study (TIS)
Traffic Surveys & Traffic Counts
Parking Demand Assessment
Transportation Modeling
Trip Generation & Distribution
Access & Accessibility Analysis
Junction Capacity Assessment
Future Traffic Forecasting
VISUM Transportation Modeling
VISSIM Microsimulation Analysis
Traffic Mitigation Strategies
Parking Mitigation Evaluation''',
                'software_tools': '''PTV VISSIM
PTV VISUM
Synchro
Transportation Forecasting Models''',
                'key_elements': '''Existing traffic conditions assessment
Traffic counts and intersection analysis
Parking supply and demand evaluation
Public transit accessibility analysis
Trip generation using Kuwait Trip Generation Manual
Future traffic forecasting for 2030 & 2040
Transportation model development using Kuwait National Model
VISUM sub-area model extraction and calibration
VISSIM operational assessment for major intersections
Mitigation measures for critical bottlenecks
Future "With Project" and "Without Project" scenario analysis''',
            },
            {
                'name': 'Canadian University Kuwait',
                'category': global_category,
                'location': 'Kuwait',
                'description': 'Comprehensive Traffic Impact Study for a modern educational campus.',
                'about': 'CEPAC conducted a comprehensive Traffic Impact Study (TIS) for the proposed Canadian University Kuwait development to evaluate the project\'s impact on the surrounding transportation network and ensure efficient mobility and accessibility for students, staff, and visitors. The study incorporated transportation modeling, trip generation and distribution analysis, future traffic forecasting, and mitigation assessments to support safe and sustainable campus operations.',
                'services': '''Traffic Impact Study (TIS)
Transportation Planning
Traffic Surveys & Traffic Counts
Parking Demand Assessment
Trip Generation & Distribution
Access & Circulation Analysis
Junction Capacity Assessment
Future Traffic Forecasting
Transportation Modeling
Traffic Mitigation Strategies
Microsimulation Analysis
Road Network Evaluation''',
                'software_tools': '''PTV VISSIM
PTV VISUM
Synchro
Transportation Forecasting Models
Traffic Simulation Tools''',
                'key_elements': '''Existing traffic conditions assessment
Peak hour traffic analysis
Traffic volume surveys
Parking supply & demand evaluation
Campus accessibility assessment
Internal circulation analysis
Trip generation estimation
Trip distribution & assignment
Transportation network modeling
Future "With Project" and "Without Project" scenarios
Intersection operational analysis
Level of Service (LOS) evaluation
Traffic mitigation and improvement proposals''',
            },
            {
                'name': 'Al-Aknan Residential Complex',
                'category': global_category,
                'location': 'Salmiya – Hawalli Governorate – Kuwait',
                'description': 'Large-scale mixed-use residential development Traffic Impact Study.',
                'about': 'CEPAC conducted a comprehensive Traffic Impact Study (TIS) for the proposed Al-Aknan Residential Complex located in Salmiya, Hawalli Governorate, Kuwait. The study evaluated the transportation impact of a large-scale mixed-use residential development consisting of residential towers, retail facilities, clinics, clubs, and integrated community services distributed across Plots 5, 7, and 8.',
                'services': '''Traffic Impact Study (TIS)
Transportation Planning
Traffic Surveys & Traffic Counts
Parking Demand & Supply Assessment
Trip Generation & Distribution
Transportation Modeling
Access & Circulation Analysis
Internal Road Network Evaluation
Intersection Capacity Assessment
Future Traffic Forecasting
Traffic Operations Analysis
Mitigation Strategy Development
Public Transport Accessibility Evaluation
Microsimulation & Operational Assessment''',
                'software_tools': '''PTV VISUM
Traffic Forecasting Models
AutoTURN
Transportation Modeling Tools
Kuwait National Transport Model (KNTM)''',
                'key_elements': '''Existing traffic conditions assessment
Peak hour traffic analysis
Traffic volume surveys
Parking evaluation for Plots 5, 7 & 8
Accessibility assessment
Internal circulation analysis
Ramp and parking design review
Trip generation estimation
Trip distribution & assignment
Transportation network modeling
Future "With Project" and "Without Project" scenarios
Intersection operational analysis
Level of Service (LOS) evaluations
Future 2030 & 2040 forecasting
Traffic mitigation and improvement proposals
Signalized intersection optimization analysis
Public transport accessibility evaluation''',
            },
            {
                'name': 'West Al-Aziziyah',
                'category': global_category,
                'location': 'West Al-Aziziyah District, Kingdom of Saudi Arabia',
                'description': 'Traffic Impact Assessment for a development in a rapidly urbanizing area.',
                'about': 'The Traffic Impact Assessment (TIA) was conducted for the West Al-Aziziyah Development Project, located within a rapidly developing urban area characterized by mixed land-use activities and increasing transportation demand. The assessment aimed to evaluate the anticipated traffic impact of the proposed development on the surrounding road network and identify the required mitigation measures.',
                'services': '''Traffic Impact Study (TIS)
Traffic Surveys & Data Collection
Existing Traffic Conditions Assessment
Peak Hour Traffic Analysis
Transportation Modeling & Forecasting
Trip Generation & Distribution
Road Links Evaluation
Intersection Operational Analysis
Future Traffic Scenario Assessment
Mitigation Measures Development
Level of Service (LOS) Evaluation
Accessibility & Circulation Assessment
Network Performance Analysis''',
                'software_tools': '''PTV Visum
PTV VISSIM
SIDRA Intersection
Synchro
ArcGIS
Highway Capacity Software (HCS)''',
                'key_elements': '''Traffic Surveys & Data Collection
Existing Traffic Conditions Assessment
Peak Hour Traffic Analysis
Transportation Modeling & Forecasting
Trip Generation & Distribution
Road Links Evaluation
Intersection Operational Analysis
Future Traffic Scenario Assessment
Mitigation Measures Development
Level of Service (LOS) Evaluation
Accessibility & Circulation Assessment
Network Performance Analysis''',
            },
        ]

        # Create projects
        created_count = 0
        for idx, data in enumerate(projects_data):
            project, created = Project.objects.get_or_create(
                slug=slugify(data['name']),
                defaults={
                    'name': data['name'],
                    'category': data['category'],
                    'location': data['location'],
                    'description': data['description'],
                    'about': data['about'],
                    'services': data['services'],
                    'software_tools': data['software_tools'],
                    'key_elements': data.get('key_elements', ''),
                    'statistical_analysis': data.get('statistical_analysis', ''),
                    'order': idx,
                    'is_featured': idx < 3,  # First 3 are featured
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f'✓ Created: {data["name"]}')
            else:
                self.stdout.write(f'- Already exists: {data["name"]}')

        self.stdout.write(self.style.SUCCESS(f'\n✓ Portfolio populated successfully! ({created_count} new projects created)'))
