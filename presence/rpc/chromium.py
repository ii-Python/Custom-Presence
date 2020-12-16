# Modules
from fnmatch import fnmatch

# Main chromium-based title function
def get_chromium_website(config, title):

    title = title.replace("|CSPRC_CHROMIUM", "").replace("\n", "")
    browser = title.split(" - ")[-1].lower()

    if browser not in config["browsers"]:
        return None, None

    title = "".join(_ + " - " for _ in title.split(" - ")[:-1])[:-3]

    site = None
    for website in config["websites"]:
        if fnmatch(title, website["match"]):
            site = website
    
    if site is None:
        return browser, config["applications"][browser]

    data = {
        "name": site["name"],
        "text": "test"
    }
    return site["icon"], data
