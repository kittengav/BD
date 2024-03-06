window.onload = async function (){
    const animal_object = new BaseObject("animals",
        ["id", "name", "description", "type_id", "aviary_id"],
        "id",
        {aviary_id: "aviaries", type_id: "animal_types"})

    const _content = new BaseContent(animal_object)
    await _content.list_view( 0)
}

