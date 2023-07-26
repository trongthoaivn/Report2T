class StyleTrigger :
    """
    Style Trigger
    """
    
    style_name = ""
    """
    Style name flag to apply trigger
    """
    target_name = ""
    """
    Target tag name
    """
    target_option  =None
    """
    TriggerTarget constant.
    """
    callback = None
    """
    Callback function
    """

    def __init__(self, style_name=None, target_name=None, target_option=None, callback=None):
        """
        Constructor

        Args:
            style_name (str, optional):\n
                Style name flag to apply trigger. Require using pattern @{sample}@.\n
                Ex : @style1@\n
            target_name (str, optional): Target tag name.\n
            target_option (Config.TriggerTarget, optional): TriggerTarget constant.\n
            callback (function, optional): 
                Callback function to handle style based on value.\n
                Require define the callback function using pattern.\n
                Ex : 
                def trigger(value:str, style:BeautifulSoup):
                    pass
        """
        self.style_name = style_name
        self.target_name = target_name
        self.target_option = target_option
        self.callback = callback
