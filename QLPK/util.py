from flask import jsonify


def ConvertModelListToDictList(model_list):
    dict_items = []
    for item in model_list:
        dict_items.append(item.serialize())
    return dict_items


def ConvertModelListToJson(model_list):
    return jsonify(list(map(lambda item: item.serialize(), model_list)))
