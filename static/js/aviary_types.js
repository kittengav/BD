window.onload = async function (){
    const aviary_types_object = new BaseObject("aviary_types",
        ["id", "name"],
        "id",
        {})

    const _content = new BaseContent(aviary_types_object)
    await _content.list_view(0)
}