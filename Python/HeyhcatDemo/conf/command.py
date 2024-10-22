import json
import re
from typing import List, Optional
from pydantic import BaseModel

# Constants
TYPE_SUB_COMMAND = 1
TYPE_SUB_COMMAND_GROUP = 2
TYPE_STRING = 3
TYPE_NUMBER= 4
TYPE_BOOLEAN = 5
TYPE_USER = 6
TYPE_CHANNEL = 7
TYPE_ROLE = 8
TYPE_SELECT = 9
TYPE_INTEGER  = 10


class CommandInfo(BaseModel):
    id: str
    name: str
    type: int
    options: Optional[List['Options']] = None


class Options(BaseModel):
    value: str
    name: str
    choices: Optional[List['Options']] = None
    type: int

def json_parser(path:str) -> dict:
    """
    Parse json file by path; return dict object
    """
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return data

############ TEST Code ############
if __name__ == "__main__":
    msg = '/roll 1d100 - 10 &lt; 40'
    html_compa = ['&lt;', '&gt;', '&le;', '&ge;']
    raw_compa = ['<', '>', '<=', '>=']
    for i in range(len(html_compa)):
        msg = msg.replace(html_compa[i], raw_compa[i])
        
    print(msg)
    find_patter = r"[><=]{1,2}\s?\d+"
    find_list = re.findall(find_patter, msg)
    print(find_list)
