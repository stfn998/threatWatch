from enum import Enum

class AccountStatus(Enum):
    CONFIRMED = "confirmed"
    DISABLED = "disabled"
    PENDING = "pending"

class IndustryType(Enum):
    AUTOMOTIVE = "automotive"
    CHEMICAL = "chemical"
    EDUCATION = "education"
    ELECTRO_MANUFACTURING = "electronic manufacturing"
    FINANCE = "finance"
    FOOD = "food and beverage"
    GOVERNMENT = "government"
    MEDIA = "media and entertainment"
    METALS = "metals"
    MINING = "mining"
    OTHER = "other"
    PETROLEUM = "petroleum"
    PHARMACEUTICAL = "pharmaceutical"
    POWER = "power and utilities"
    PAPER = "pulp and paper"
    TECHNOLOGY = "technology"
    TRANSPORTATION = "transportation"
    WATER = "water/waste water"

class IncidentReliability(Enum):
    CONFIRMED = "confirmed"
    FALSE = "false"
    FALSE_POSITIVE = "false positive"
    OPEN = "open"
    SUSPECTED = "suspected"
    UNKNOWN = "unknown"

class IncidentType(Enum):
    DNS = "DNS tunneling"
    DOS = "denial of service"
    INJECTION = "SQL injection"
    MALWARE = "malware"
    OTHER = "other"
    PHISHING = "phishing"
    RANSOMWARE = "ransomware"
    ROOTKIT = "rootkit"
    SCRIPTING = "cross-site scripting"
    ZERO_DAY = "zero day exploit"

class Role(Enum):
    ADMIN = "administrator"
    USER = "registered_user"
