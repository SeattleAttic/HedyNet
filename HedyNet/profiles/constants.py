"""These are all constants related to access and status levels.  They will be used throughout the
website to help manage information control."""

PRIVATE_ACCESS = "private"
ADMIN_ACCESS = "admin"
MEMBERS_ACCESS = "members"
REGISTERED_ACCESS = "registered"
PUBLIC_ACCESS = "public"

"""A list of access orders from most to least constrictive."""
ACCESS_ORDER = (PRIVATE_ACCESS, ADMIN_ACCESS, MEMBERS_ACCESS, REGISTERED_ACCESS,
    PUBLIC_ACCESS)

EXTENDED_ACCESS_LEVELS = (
    (PRIVATE_ACCESS, "private"),
    (ADMIN_ACCESS, "admin"),
    (MEMBERS_ACCESS, "members"),
    (REGISTERED_ACCESS, "registered"),
    (PUBLIC_ACCESS, "public"),
)

NONPUBLIC_ACCESS_LEVELS = (
    (PRIVATE_ACCESS, "private"),
    (ADMIN_ACCESS, "admin"),
    (MEMBERS_ACCESS, "members"),
    (REGISTERED_ACCESS, "registered"),
)

ACCESS_LEVELS = (
    (ADMIN_ACCESS, "admin"),
    (MEMBERS_ACCESS, "members"),
    (PUBLIC_ACCESS, "public"),
)

BASIC_ACCESS_LEVELS = (
    (MEMBERS_ACCESS, "members"),
    (REGISTERED_ACCESS, "registered"),
    (PUBLIC_ACCESS, "public"),
)

ACTIVE_STATUS = "active"
APPLYING_STATUS = "applying"
REFUSED_STATUS = "refused"
INACTIVE_STATUS = "inactive"
REVOKED_STATUS = "revoked"

STATUS_LEVELS = (
    (ACTIVE_STATUS, "active"),
    (APPLYING_STATUS, "applying"),
    (REFUSED_STATUS, "refused"),
    (INACTIVE_STATUS, "inactive"),
    (REVOKED_STATUS, "revoked"),
)

EMAIL_CONTACT = "email"
PHONE_CONTACT = "phone"
TEXT_CONTACT = "text"

CONTACT_METHODS = (
    (EMAIL_CONTACT, "email"),
    (PHONE_CONTACT, "phone"),
    (TEXT_CONTACT, "text"),
)
