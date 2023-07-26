from Config import Libreoffice
from subprocess import Popen, PIPE
from pathlib import Path
import sys
import tempfile
import logging


# Setting logger
logging.basicConfig(level=logging.DEBUG,format = '%(asctime)s : %(levelname)s - %(message)s')

class OfficeHelper:
    """
    Office Helper class
    
    """
    def __init__(self):
        """
        Office Helper constructor
        """
        pass

    def is_exist_office_executor(self) -> bool:
        """
        Check exist Libreoffice program

        Raises:
            Exception: Could not find Libreoffice executor.

        Returns:
            [bool]: is exist Libreoffice program
        """
        try:
            os = sys.platform
            if "win32" in os :
                self.exec_command(command=Libreoffice.COMMAND_DETECT_WINDOW)
            else:
                self.exec_command(command=Libreoffice.COMMAND_DETECT_LINUX)
            return True
        except:
            raise Exception("Could not find Libreoffice executor.")
        
    def convert(self, command:str):
        """
        Execute convert command using Libreoffice executor

        Args:
            command (str): convert command

        Raises:
            Exception: Could not execute convert command.
        """
        try:
            if self.is_exist_office_executor():
                # create user profile
                temp_dir = tempfile.TemporaryDirectory()
                user_dir = Libreoffice.USER_TEMP_DIR.format(Path(temp_dir.name).as_uri())
                command += user_dir
                self.exec_command(command=command)
                temp_dir.cleanup()
        except Exception as ex:
            raise Exception(f"Could not execute convert command. (command={command}, Exception={ex})")
        
    def exec_command(self, command:str):
        """
        Execute command

        Args:
            command (str): command

        Raises:
            Exception: Execute command failed.
            Exception: Could not execute command.
        """
        logging.info(f"Execute command : {command}")
        proc = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        try:
            outs, errs = proc.communicate()
            outs = outs.decode("utf-8").splitlines()
            errs = errs.decode("utf-8").splitlines()
            logging.debug(f"Execute command returncode: {proc.returncode}")
            if proc.returncode != 0:
                raise Exception(f"Execute command failed. (returncode={proc.returncode})")
        except Exception as ex:
            raise Exception(f"Could not execute command. (command={command}, Exception={ex})")
        finally:
            logging.info(f"Execute command output:\nOutput : {outs} \nError : {errs}")