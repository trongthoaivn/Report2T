from Config import OutputFormat, Libreoffice, TriggerTarget
from OfficeHelper import OfficeHelper
from StyleTrigger import StyleTrigger
from jinja2 import Template
from bs4 import BeautifulSoup
from typing import List
import os
import logging
import re
import copy
import random
import string
import base64


# Setting logger
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s : %(levelname)s - %(message)s"
)


class Report2T:
    """
    Report2T
    """

    input_file_path = ""
    """
    input file path
    """
    output_dir_path = ""
    """
    output directory path
    """
    convert_to_format = ""
    """
    convert format
    """
    list_style_trigger: List[StyleTrigger] = []
    """
    list style trigger
    """
    image_list: List[tuple[str, str]] = []
    data = None
    """
    data 
    """

    helper = OfficeHelper()

    def __init__(
        self,
        input_file_path: str,
        output_dir_path: str,
        convert_to_format: OutputFormat,
        data=None,
    ):
        """
        Constructor

        Args:
            input_file_path (str): input file path
            output_dir_path (str): output directory path
            convert_to_format (OutputFormat): convert format
            data (dict, optional): data
        """
        self.input_file_path = input_file_path
        self.output_dir_path = output_dir_path
        self.convert_to_format = convert_to_format
        self.data = data

    def add_style(self, style_trigger: StyleTrigger):
        """
        Append style trigger

        Args:
            style_trigger (StyleTrigger): style trigger object
        """
        self.list_style_trigger.append(style_trigger)

    def __apply_style(self, xml_str: str) -> str:
        """
        Apply style trigger

        Args:
            xml_str (str): xml string

        Raises:
            Exception: Target option not found!
            Exception: Could not apply style trigger.

        Returns:
            str: xml string applied
        """
        try:
            # xml object
            xml_obj = BeautifulSoup(xml_str, "xml")
            # get list style of xml object
            xml_list_style_obj = xml_obj.find("office:automatic-styles")

            # for loop in list style trigger
            for style_trigger in self.list_style_trigger:
                # get target style name of xml object
                xml_target_obj = xml_obj.find(
                    style_trigger.target_name,
                    string=re.compile(f"@{style_trigger.style_name}@"),
                )
                if xml_target_obj is None:
                    logging.warning(
                        f"Could not find target object. (style_name={style_trigger.style_name})"
                    )
                    break
                # get current value of xml target object
                target_value = xml_target_obj.string.replace(
                    f"@{style_trigger.style_name}@", ""
                )
                # remove style name of xml target object
                xml_target_obj.string = target_value
                # get current style name of xml target object
                current_style_name = ""
                match style_trigger.target_option:
                    case TriggerTarget.SELF:
                        current_style_name = xml_target_obj.attrs.get(
                            f"{xml_target_obj.prefix}:style-name"
                        )
                    # target style is parent style
                    case TriggerTarget.PARENT:
                        xml_target_obj = xml_target_obj.parent
                        current_style_name = xml_target_obj.attrs.get(
                            f"{xml_target_obj.prefix}:style-name"
                        )
                    case _:
                        raise Exception("Target option not found!")
                # clone current style of xml target object
                xml_current_style = xml_obj.find(
                    "style:style", attrs={"style:name": current_style_name}
                )
                xml_style_clone = copy.copy(xml_current_style)
                # callback trigger function
                if style_trigger.callback is not None:
                    style_trigger.callback(target_value, xml_style_clone)
                # set new style to xml object
                xml_style_name_clone = "".join(
                    random.choice(string.ascii_letters) for i in range(8)
                )
                xml_target_obj[
                    f"{xml_target_obj.prefix}:style-name"
                ] = xml_style_name_clone
                xml_style_clone["style:name"] = xml_style_name_clone
                xml_list_style_obj.append(xml_style_clone)

            # return xml content
            return str(xml_obj)
        except Exception as ex:
            raise Exception(f"Could not apply style trigger. (Exception={ex})")

    def add_image(self, image_name: str, file_path: str):
        """
        Add image

        Args:
            image_name (str): image name
            file_path (str): file path
        """
        self.image_list.append((image_name, file_path))

    def __replace_image(self, xml_str: str) -> str:
        """
        Replace image

        Args:
            xml_str (str): xml string

        Raises:
            Exception: Could not replace image.

        Returns:
            str: xml string replaced
        """

        try:
            # xml object
            xml_obj = BeautifulSoup(xml_str, "xml")
            # for loop in image list
            for image in self.image_list:
                image_name = image[0]
                file_path = image[1]
                if not os.path.exists(file_path):
                    logging.warning(
                        f"File path is not exist. (image_name={image_name},file_path={file_path})"
                    )
                    break
                # get xml draw frame object
                draw_frame_target = xml_obj.find(
                    "draw:frame", attrs={"draw:name": f"{image_name}"}
                )
                if draw_frame_target is None:
                    logging.warning(
                        f"Image name is not exist. (image_name={image_name}"
                    )
                    break
                # read image
                file = open(file_path, "rb")
                # base64 encode
                base64_data = base64.b64encode(file.read())
                file.close()
                # write image to draw frame
                xml_bin_obj = draw_frame_target.find("office:binary-data")
                xml_bin_obj.string = base64_data.decode("utf-8")

            # return xml content
            return str(xml_obj)
        except Exception as ex:
            raise Exception(f"Could not replace image. (Exception={ex})")

    def __bind_data(self):
        """
        Binding data to template

        Raises:
            Exception: Target file does not exist.
            Exception: Could not binding data template .
        """
        try:
            # convert template to xml format
            format = {
                "output_format": OutputFormat.XML,
                "output_dir": self.output_dir_path,
                "input_file": self.input_file_path,
            }
            command = Libreoffice.COMMAND_CONVERT_WINDOW.format_map(format)
            self.helper.convert(command)

            # xml template file path
            dirname = os.path.dirname(self.input_file_path)
            filename = (
                os.path.basename(self.input_file_path).split(".")[0]
                + f".{OutputFormat.XML}"
            )
            template_file_path = os.path.join(dirname, filename)

            # check exist xml template
            if not os.path.exists(template_file_path):
                raise Exception(
                    f"Target file does not exist. (filepath={template_file_path})"
                )

            # write data to xml template
            with open(template_file_path, encoding="utf-8", mode="r+") as file:
                # read xml template
                template = Template(file.read())
                # binding data
                template_content = template.render(data=self.data)
                # apply style trigger
                template_content = self.__apply_style(template_content)
                # replace image
                template_content = self.__replace_image(template_content)
                # write xml file content
                file.seek(0)
                file.write(template_content)
                file.truncate()
                file.close()

            # set template path is xml template
            self.input_file_path = template_file_path
        except Exception as ex:
            raise Exception(
                (
                    f"Could not binding data template . (filepath={self.input_file_path}, Exception={ex})"
                )
            )

    def exec_convert(self):
        """
        Convert template file to output format

        Raises:output_dir_path
            Exception: Could not execute convert .
        """
        command = ""
        try:
            # binding data to template
            self.__bind_data()
            # execute convert command
            format = {
                "output_format": self.convert_to_format,
                "output_dir": self.output_dir_path,
                "input_file": self.input_file_path,
            }
            command = Libreoffice.COMMAND_CONVERT_WINDOW.format_map(format)
            self.helper.convert(command)

            # remove temp files
            #os.remove(self.input_file_path)
        except Exception as ex:
            raise Exception(
                f"Could not execute convert . (command={command}, Exception={ex}))"
            )
