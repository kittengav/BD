window.onload = async function (){
    const animal_types_object = new BaseObject("animal_types",
        ["id", "name", "description"],
        "id",
        {})

    const _content = new BaseContent(animal_types_object)
    await _content.list_view( 0)
}