import re


def slugify_org_name(organization_name: str) -> str:
    """
    Convert organization name to a safe collection name.
    Pattern: org_<slugged_name>
    """
    # Convert to lowercase
    slug = organization_name.lower()
    # Replace spaces and hyphens with underscores
    slug = slug.replace(' ', '_').replace('-', '_')
    # Remove special characters, keep only alphanumeric and underscores
    slug = re.sub(r'[^a-z0-9_]', '', slug)
    # Remove multiple consecutive underscores
    slug = re.sub(r'_+', '_', slug)
    # Remove leading/trailing underscores
    slug = slug.strip('_')
    return f"org_{slug}"

