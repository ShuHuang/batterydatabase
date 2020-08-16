import re

def extract_value(string):
    """
    Takes a string and returns a list of floats representing the string given.
    Usage::
        test_string = '150 to 160'
        end_value = extract_value(test_string)
        print(end_value) # [150., 160.]
    :param str string: A representation of the values as a string
    :returns: The value expressed as a list of floats of length 1 if the value had no range,
        and as a list of floats of length 2 if it was a range.
    :rtype: list(float)
    """
    if string is None:
        return None
    string = string.replace("-", "-")
    string = string.replace("–", "-")
    string = string.replace("−", "-")
    string = string.split("±")[0]
    split_by_space = [r for r in re.split(' |(-)', string) if r]
    split_by_num = []
    for elem in split_by_space:
        split_by_num.extend([r for r in re.split('(\d+\.?(?:\d+)?)', elem) if r])
    try:
        if split_by_num[0] == "-":
            split_by_num[0] = "-" + split_by_num.pop(1)
    except:
        pass
    flag = 0
    new_split_by_num = []
    for index, value in enumerate(split_by_num):
        if flag == 2:
            new_split_by_num.append(split_by_num[index - 2])
            new_split_by_num.append(split_by_num[index - 1] + value)
            flag = 0
        elif flag == 1 and re.match('(-?\d+\.?(?:\d+)?)', value):
            new_split_by_num.append(split_by_num[index - 1])
            new_split_by_num.append(value)
            flag = 0
        elif not re.match('(-?\d+\.?(?:\d+)?)', value):
            flag += 1
        else:
            new_split_by_num.append(value)
    values = []
    for index, value in enumerate(new_split_by_num):
        try:
            float_val = float(value)
            values.append(float_val)
        except ValueError:
            pass

    return values

def extract_capa_units(string):
    """
    Takes a string and returns a list of floats representing the string given. Temporary capacity unit model.
    Usage::
        test_string = 'mAh/g'
        end_value = extract_value(test_string)
        print(end_value) # "Gram^(-1.0)  Hour^(1.0)  MilliAmpere^(1.0)"
    :param str string: A representation of the units as a string
    :returns: The unit model
    :rtype: string
    """
    if string == "Ah/kg" or string == "Ahkg-1":
        return "Ampere^(1.0) Hour^(1.0) KiloGram^(-1.0)"
    elif string == "Ah/g" or string == "Ahg-1":
        return "Ampere^(1.0)  Gram^(-1.0)  Hour^(1.0)"
    elif string == "mAh/kg" or string == "mAhkg-1":
        return "Hour^(1.0)  KiloGram^(-1.0)  MilliAmpere^(1.0)"
    else:
        return "Gram^(-1.0)  Hour^(1.0)  MilliAmpere^(1.0)"

def extract_volt_units(string):
    """
    Takes a string and returns a list of floats representing the string given. Temporary voltage unit model.
    Usage::
        test_string = 'mAh/g'
        end_value = extract_value(test_string)
        print(end_value) # "Gram^(-1.0)  Hour^(1.0)  MilliAmpere^(1.0)"
    :param str string: A representation of the units as a string
    :returns: The unit model
    :rtype: string
    """
    if string == "mV":
        return "MilliVolt^(1.0)"
    else:
        return "Volt^(1.0)"

def extract_coul_units(string):
    """
    Takes a string and returns a list of floats representing the string given. Temporary capacity unit model.
    Usage::
        test_string = 'mAh/g'
        end_value = extract_value(test_string)
        print(end_value) # "Gram^(-1.0)  Hour^(1.0)  MilliAmpere^(1.0)"
    :param str string: A representation of the units as a string
    :returns: The unit model
    :rtype: string
    """
    return "Percent^(1.0)"

def extract_cond_units(string):
    """
    Takes a string and returns a list of floats representing the string given. Temporary capacity unit model.
    Usage::
        test_string = 'mAh/g'
        end_value = extract_value(test_string)
        print(end_value) # "Gram^(-1.0)  Hour^(1.0)  MilliAmpere^(1.0)"
    :param str string: A representation of the units as a string
    :returns: The unit model
    :rtype: string
    """
    if string == "mS/cm" or string == "mScm-1":
        return "CentiMeter^(-1.0)  MilliSiemens^(1.0)"
    elif string == "mS/m" or string == "mSm-1":
        return "Meter^(-1.0)  MilliSiemens^(1.0)"
    else:
        return "CentiMeter^(-1.0)  Siemens^(1.0)"

def extract_ener_units(string):
    """
    Takes a string and returns a list of floats representing the string given. Temporary capacity unit model.
    Usage::
        test_string = 'mAh/g'
        end_value = extract_value(test_string)
        print(end_value) # "Gram^(-1.0)  Hour^(1.0)  MilliAmpere^(1.0)"
    :param str string: A representation of the units as a string
    :returns: The unit model
    :rtype: string
    """
    if string == "Wh/g" or string == "Whg-1":
        return "Gram^(-1.0)  WattHour^(1.0)"
    else:
        return "KiloGram^(-1.0)  WattHour^(1.0)"