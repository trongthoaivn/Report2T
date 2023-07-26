import enum
class OutputFormat():
    """
    Output format
    """
    XML = "xml"
    """
    Convert to xml format
    """
    PDF = "pdf"
    """
    Convert to pdf format
    """

class Libreoffice():
    """
    Libreoffice helper
    """
    
    # command check version
    COMMAND_DETECT_LINUX = "lireoffice --version"
    """
    Command detect libreoffice Linux os
    """
    COMMAND_DETECT_WINDOW = "soffice.com --version"
    """
    Command detect libreoffice Window os
    """
    
    # command convert 
    COMMAND_CONVERT_LINUX = """soffice --headless --invisible --nodefault --nolockcheck --nologo --norestore --nofirststartwizard --convert-to {output_format} --outdir "{output_dir}" "{input_file}" """
    """
    Command convert using libreoffice Linux os
    """
    COMMAND_CONVERT_WINDOW = """soffice.com --headless --invisible --nodefault --nolockcheck --nologo --norestore --nofirststartwizard --convert-to {output_format} --outdir "{output_dir}" "{input_file}" """
    """
    Command convert using libreoffice Window os
    """
    
    # config user temp directory path
    USER_TEMP_DIR = """-env:UserInstallation={0}"""
    """
    Config user temporary directory path
    """

class TriggerTarget():
    """
    Trigger target
    """
    SELF = 0
    """
    Target style is self object
    """
    PARENT = 1
    """
    Target style is parent object
    """
    