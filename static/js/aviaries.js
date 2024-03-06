window.onload = async function (){
    const aviary_object = new BaseObject("aviaries",
        ["id", "name", "type_id"],
        "id",
        {type_id: "aviary_types"})

    const _content = new BaseContent(aviary_object)
    await _content.list_view(0)
}