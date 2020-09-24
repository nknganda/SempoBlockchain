import re
from toolz import pipe, curry

from server.constants import KOBO_META_ATTRIBUTES, DEFAULT_ATTRIBUTES
from server.models.settings import Settings
from server.models.attribute_map import AttributeMap

def standard_user_preprocess(attribute_dict, SETTINGS):
    """
    The standard flow when preprocessing user data. Note: order is carefully chosen
    eg data is unwrapped before any other processing
    """
    return pipe(
        attribute_dict,
        unwrap_data,
        map_attribute_keys,
        filter_out_kobo_meta_attributes,
        filter_out_underscore_prefixed_attributes,
        force_attribute_dict_keys_to_lowercase,
        strip_preslashes,
        attempt_to_truthy_values,
        strip_weirdspace_characters,
        convert_unknown_attributes_to_custom_attributes,
        insert_settings_from_database(SETTINGS),
    )


def unwrap_data(attribute_dict):
    """
    Allows the use of wrapped data payloads by taking the contents of _data and moving it up a level.
    This is useful for setting default values in the wrapper in tools such as Kobo toolbox.
    In the event of a conflict between two levels, the wrapped data takes priority.
    {'is_vendor': True, '_data': {'first_name': 'Alice'}} -> {'is_vendor': True, 'first_name': 'Alice'}
    """
    _data = attribute_dict.get('_data')
    if isinstance(_data, dict):
        attribute_dict = {**attribute_dict, **_data}
        attribute_dict.pop('_data')

    return attribute_dict


def map_attribute_keys(attribute_dict):
    """
    Allows custom re-mapping of keys.
    {'your_first_name': 'Alice'} -> {'first_name': 'Alice}
    """
    map_values = AttributeMap.query.all()
    map_dict = {}
    for mval in map_values:
        map_dict[mval.input_name] = mval.output_name

    return {map_dict.get(k, k): v for k, v in attribute_dict.items()}


def filter_out_kobo_meta_attributes(attribute_dict):
    for k in KOBO_META_ATTRIBUTES:
        attribute_dict.pop(k, None)

    return attribute_dict


def filter_out_underscore_prefixed_attributes(attribute_dict):

    attribute_dict = {k: v for k, v in attribute_dict.items() if k[0] != '_'}

    for key in attribute_dict.keys():
        if key[0] == '_':
            del attribute_dict[key]

    return attribute_dict


def convert_unknown_attributes_to_custom_attributes(attribute_dict):

    custom_attributes = attribute_dict.get('custom_attributes', {})
    for key in attribute_dict.keys():
        if key not in DEFAULT_ATTRIBUTES:
            custom_attributes[key] = attribute_dict[key]

    if custom_attributes:
        attribute_dict['custom_attributes'] = custom_attributes

    for k in custom_attributes.keys():
        attribute_dict.pop(k, None)

    return attribute_dict


def force_attribute_dict_keys_to_lowercase(attribute_dict):
    return dict(zip(map(str.lower, attribute_dict.keys()), attribute_dict.values()))


def strip_preslashes(attribute_dict):
    return dict(
        zip(
            map(lambda key: key[_return_index_of_slash_or_neg1(key) + 1:], attribute_dict.keys()),
            attribute_dict.values()
        )
    )


@curry
def insert_settings_from_database(settings_list, attribute_dict):
    for setting in settings_list:
        if setting not in attribute_dict:
            stored_setting = Settings.query.filter_by(name=setting).first()

            if stored_setting is not None:
                attribute_dict[setting] = stored_setting.value

    return attribute_dict


def attempt_to_truthy_values(attribute_dict):
    return dict(
        zip(attribute_dict.keys(), map(_convert_yes_no_string_to_bool, attribute_dict.values())))


def strip_weirdspace_characters(attribute_dict):

    return dict(
        zip(
            map(_remove_wierdspaces_from_string, attribute_dict.keys()),
            map(_remove_wierdspaces_from_string, attribute_dict.values())
        )
    )

def _return_index_of_slash_or_neg1(string):
    try:
        return str(string).index("/")
    except ValueError:
        return -1


def _convert_yes_no_string_to_bool(test_string):
    if str(test_string).lower() in ["yes", "true"]:
        return True
    elif str(test_string).lower() in ["no", "false"]:
        return False
    else:
        return test_string


def _remove_wierdspaces_from_string(maybe_string):
    """
    removes tabs, newlines and returns, but NOT plain old spaces
    """
    if isinstance(maybe_string, str):
        return re.sub(r'[\t\n\r]', '', maybe_string)
    else:
        return maybe_string