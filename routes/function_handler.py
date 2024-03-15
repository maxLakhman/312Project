def escape_html(string):
    string = string.replace("&", "&amp;")
    string = string.replace("<", "&lt;")
    string = string.replace(">", "&gt;")
    return string
