from datetime import date, datetime

DATE_FORMAT = "%d/%m/%Y"         
LEVELS = ["Undergraduate", "Masters", "PhD"]
ANY = "Any"                      
ALL_AFRICA = "All Africa"          


def format_date(d):
    return d.strftime(DATE_FORMAT)


class Scholarship:

    def __init__(self, name, provider, country, level, field,
                 eligibility, deadline, link, date_checked=None, scholarship_id=None):
        self.id = scholarship_id
        self.name = name
        self.provider = provider
        self.country = country          
        self.level = level              
        self.field = field              
        self.eligibility = eligibility  
        self.deadline = deadline        
        self.link = link                
        self.date_checked = date_checked or date.today()

    @classmethod
    def from_row(cls, row):
        (sid, name, provider, country, level, field,
         eligibility, deadline, link, date_checked) = row
        return cls(name, provider, country, level, field, eligibility,
                   datetime.strptime(deadline, "%Y-%m-%d").date(), link,
                   datetime.strptime(date_checked, "%Y-%m-%d").date(), sid)

    def days_left(self):
        return (self.deadline - date.today()).days

    def is_open(self):
        return self.days_left() >= 0

    def status(self):
        return "Open" if self.is_open() else "Closed"

    def matches(self, profile):
        country_ok = self.country.lower() in (profile.home_country.lower(), ALL_AFRICA.lower())
        level_ok = self.level.lower() in (profile.level.lower(), ANY.lower())
        field_ok = self.field.lower() in (profile.field.lower(), ANY.lower())
        return country_ok and level_ok and field_ok and self.is_open()

    def table_row(self):
        name = self.name if len(self.name) <= 30 else self.name[:27] + "..."
        return f"{self.id:<4}{name:<31}{self.country:<12}{format_date(self.deadline):<12}{self.status()}"

    def details_text(self):
        left = self.days_left()
        if left >= 0:
            timing = f"{left} day(s) left"
        else:
            timing = f"closed {-left} day(s) ago"
        return (
            f"ID:            {self.id}\n"
            f"Name:          {self.name}\n"
            f"Provider:      {self.provider}\n"
            f"Country:       {self.country}\n"
            f"Level:         {self.level}\n"
            f"Field:         {self.field}\n"
            f"Eligibility:   {self.eligibility}\n"
            f"Deadline:      {format_date(self.deadline)} ({timing})\n"
            f"Official link: {self.link}\n"
            f"Date checked:  {format_date(self.date_checked)}"
        )


TABLE_HEADER = f"{'ID':<4}{'Scholarship':<31}{'Country':<12}{'Deadline':<12}Status"


class StudentProfile:

    def __init__(self, home_country, level, field):
        self.home_country = home_country
        self.level = level
        self.field = field


class Notification:

    def __init__(self, message, kind, date_created=None, is_read=False, notification_id=None):
        self.id = notification_id
        self.message = message
        self.kind = kind                
        self.date_created = date_created or date.today()
        self.is_read = is_read

    def line(self):
        flag = "NEW " if not self.is_read else "    "
        return f"{flag}[{self.kind.upper():<8}] {format_date(self.date_created)}  {self.message}"
