from enum import Enum

# Application Constants
APP_NAME = "SMHunt Client Acquisition Agent"
APP_VERSION = "1.0.0"
APP_URL = "https://smhunt.online"
AGENCY_URL = "https://sm-agency.vercel.app"
SUPPORT_EMAIL = "smagencyglobel@gmail.com"
NOREPLY_EMAIL = "noreply@smhunt.online"

# Business Niches (High Priority Industries)
HIGH_PRIORITY_NICHES = [
    "Dental Clinics",
    "Law Firms",
    "Medical Clinics",
    "Real Estate Agencies",
    "Construction Companies",
    "Home Services",
    "Restaurants",
    "Beauty Salons",
    "Fitness Centers",
    "Local Professional Services"
]

# Target Countries
TARGET_COUNTRIES = [
    "USA",
    "UK", 
    "Canada",
    "Australia",
    "Germany",
    "France",
    "Netherlands",
    "Switzerland",
    "Sweden",
    "Norway"
]

# Lead Status Types
class LeadStatus(str, Enum):
    NEW = "new"
    QUALIFIED = "qualified"
    CONTACTED = "contacted"
    INTERESTED = "interested"
    NOT_INTERESTED = "not_interested"
    MEETING_BOOKED = "meeting_booked"
    CLIENT = "client"
    ARCHIVED = "archived"

# Outreach Status Types
class OutreachStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    OPENED = "opened"
    REPLIED = "replied"
    BOUNCED = "bounced"
    UNSUBSCRIBED = "unsubscribed"

# Meeting Status Types
class MeetingStatus(str, Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"

# Lead Score Categories
class LeadScoreCategory(str, Enum):
    PRIORITY_CLIENT = "priority_client"
    GROWTH_CLIENT = "growth_client"
    LOW_PRIORITY = "low_priority"

# Website Analysis Categories
class WebsiteIssue(str, Enum):
    NO_WEBSITE = "no_website"
    SLOW_LOADING = "slow_loading"
    MOBILE_ISSUES = "mobile_issues"
    SEO_PROBLEMS = "seo_problems"
    DESIGN_OUTDATED = "design_outdated"
    BROKEN_LINKS = "broken_links"
    NO_CONTACT_FORM = "no_contact_form"
    NO_ANALYTICS = "no_analytics"

# Communication Channels
class CommunicationChannel(str, Enum):
    EMAIL = "email"
    LINKEDIN = "linkedin"
    FACEBOOK = "facebook"
    PHONE = "phone"
    WEBSITE_CHAT = "website_chat"

# Data Sources
class DataSource(str, Enum):
    GOOGLE_MAPS = "google_maps"
    YELP = "yelp"
    YELLOW_PAGES = "yellow_pages"
    LINKEDIN = "linkedin"
    FACEBOOK = "facebook"
    INDUSTRY_DIRECTORY = "industry_directory"
    MANUAL_ENTRY = "manual_entry"

# AI Model Providers
class AIProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    CUSTOM = "custom"

# Email Providers
class EmailProvider(str, Enum):
    SENDGRID = "sendgrid"
    MAILGUN = "mailgun"
    SMTP = "smtp"
    AMAZON_SES = "amazon_ses"

# Follow-up Types
class FollowUpType(str, Enum):
    INITIAL_OUTREACH = "initial_outreach"
    FIRST_FOLLOWUP = "first_followup"
    SECOND_FOLLOWUP = "second_followup"
    WARM_FOLLOWUP = "warm_followup"
    AUDIT_DELIVERY = "audit_delivery"

# Intent Classification
class IntentType(str, Enum):
    INTERESTED = "interested"
    PRICING_QUESTION = "pricing_question"
    REQUEST_MEETING = "request_meeting"
    NOT_INTERESTED = "not_interested"
    NEEDS_FOLLOWUP = "needs_followup"
    UNSUBSCRIBE = "unsubscribe"

# Priority Levels
class PriorityLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

# Opportunity Types
class OpportunityType(str, Enum):
    WEBSITE_DEVELOPMENT = "website_development"
    SEO_IMPROVEMENT = "seo_improvement"
    DIGITAL_MARKETING = "digital_marketing"
    SOCIAL_MEDIA_MANAGEMENT = "social_media_management"
    PPC_ADVERTISING = "ppc_advertising"
    CONTENT_CREATION = "content_creation"
    BRAND_IDENTITY = "brand_identity"
    LOCAL_SEO = "local_seo"

# System Status
class SystemStatus(str, Enum):
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"
    MAINTENANCE = "maintenance"

# API Rate Limits
API_RATE_LIMITS = {
    "google_maps": "100/minute",
    "linkedin": "50/minute", 
    "email_sending": "500/day",
    "website_analysis": "200/minute"
}