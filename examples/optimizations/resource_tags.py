from sedai import resource

def show_resource_tags(resource_id: str):
    tags = resource.get_resource_tags(resource_id)
    for i in tags:
        print(f"key:{i['key']}, value:{i['value']}")


resource_id = "resource_id"
show_resource_tags(resource_id)