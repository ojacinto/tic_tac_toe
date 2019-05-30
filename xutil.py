#  #!/usr/bin/env python3
#  -- coding: utf-8 --
#  ---------------------------------------------------------------------------------
#  Copyright (c) 2019. Oraldo Jacinto Simon
#  #----------------------------------------------------------------------------------
#  All rights reserved.
#  #
#  This is free software; you can do what the LICENCE file allows you to.


def capture_prompt(message='', value=None):
    """Function to wait for console input.

    """
    if value:
        validated = False
        while not validated:
            prompt_input = input(message)
            validated = value(prompt_input)
        return prompt_input
    else:
        return input(message)


def convert_to_int(value):
    try:
        return int(value)
    except:
        raise TypeError


def validate_value(val):
    try:
        value = convert_to_int(val)
        return True if value in [1, 2] else False
    except:
        return False

