const host = "http://localhost:8000/api/v1"

const urls = {
    animals: `${host}/animals`,
    animal_types: `${host}/animal_types`,
    aviaries: `${host}/aviaries`,
    aviary_types: `${host}/aviary_types`
}

async function sendRequest(url = "", method = "GET", data = null) {
    console.log(url)
  let response
  if (data === null){
      response = await fetch(url, {
        method: method,
      });
  }
  else {
      response = await fetch(url, {
        method: method,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
  }
  return await response.json();
}

function BaseContent(base_object){
    this.content = document.querySelector(["div.content"])
    this.filters = [base_object.pk_field]
    let throw_pointer = this

    this.page = 0
    this.list_view = async function(page){
        let html = ""
        this.page = page
        html += '<p class="filter_title">Фильтры</p>'
        for (let f of base_object.fields){
            if (this.filters.includes(f)){
                if (f in base_object.fk_objects){
                    html += `<p  class="filter_label">${f.slice(0, -3)}: <input type="checkbox" checked="checked" class="filters" id="filt_${f}"/></p>`
                }
                else{
                    html += `<p class="filter_label">${f}: <input type="checkbox" checked="checked" class="filters" id="filt_${f}"/></p>`
                }

            }
            else{
                if (f in base_object.fk_objects){
                    html += `<p class="filter_label">${f.slice(0, -3)}: <input type="checkbox" class="filters" id="filt_${f}"/></p>`
                }
                else{
                    html += `<p class="filter_label">${f}: <input type="checkbox" class="filters" id="filt_${f}"/></p>`
                }

            }
        }
        html += `<button class="create">Создать</button>`
        await base_object.get_list(this.filters, page)
        let list = await base_object.list_html()
        html += list
        if (this.page != 0){
            html += `<button class="prev">Предыдущая</button>`
        }
        html += `<span class="page_nm">${this.page + 1}</span><button class="next">Следующая</button>`
        this.content.innerHTML = html
        let _filters = document.querySelectorAll([".filters"])

        for (let f of _filters){
            f.onchange = async function(){
                if (this.checked && !throw_pointer.filters.includes(this.id.slice(5))){
                    throw_pointer.filters.push(this.id.slice(5))
                }
                else if (this.checked == false){
                    throw_pointer.filters.splice(throw_pointer.filters.indexOf(this.id.slice(5)), 1)
                }
                await throw_pointer.list_view(throw_pointer.page)
            }
        }
        let delete_buttons = document.querySelectorAll(["button.delete"])
        for (let b of delete_buttons){
            b.onclick = async function(){
                await base_object.delete_object(b.id.slice(4))
                await throw_pointer.list_view(throw_pointer.page)
            }
        }
        let next_button = document.querySelector(["button.next"])
            next_button.onclick = async function(){
                await throw_pointer.list_view(throw_pointer.page + 1)
            }

        if (this.page != 0){
            let prev_button = document.querySelector(["button.prev"])
            prev_button.onclick = async function(){
                await throw_pointer.list_view(throw_pointer.page - 1)
            }
        }


        let retrieve_buttons = document.querySelectorAll(["button.retrieve"])
        for (let b of retrieve_buttons){
            b.onclick = async function(){
                await throw_pointer.detail_view(await base_object.get_object(b.id.slice(4)))
            }
        }

        let edit_buttons = document.querySelectorAll(["button.edit"])
        for (let b of edit_buttons){
            b.onclick = async function(){
                let obj = await base_object.get_object(b.id.slice(3))
                await throw_pointer.form_view(obj)
            }
        }

        let create_button = document.querySelector(["button.create"])
        create_button.onclick = async function(){
            await throw_pointer.form_view(null)
        }
    }

    this.detail_view = async function(obj){
        let html = ""
        html += await base_object.single_view(obj)
        this.content.innerHTML = html
        let edit_button = document.querySelector(["button.edit"])
        edit_button.onclick = async function(){
                await throw_pointer.form_view(await base_object.get_object(edit_button.id.slice(3)))
            }

        let delete_button = document.querySelector(["button.delete"])
        delete_button.onclick = async function(){
                await base_object.delete_object(delete_button.id.slice(4))
                await throw_pointer.list_view(throw_pointer.page)
            }

        let list_button = document.querySelector(["button.list"])
        list_button.onclick = async function(){
            await throw_pointer.list_view(throw_pointer.page)
        }
    }

    this.form_view = async function(obj){
        let html = ""
        html += await base_object.object_form_html(obj)
        this.content.innerHTML = html
        let cancel_button = document.querySelector(["button.cancel"])
        cancel_button.onclick = async function(){
            if (obj == null){
                await throw_pointer.list_view(throw_pointer.page)
            }
            else{
                await throw_pointer.detail_view(obj)
            }
        }

        let save_button = document.querySelector(["button.save"])

        save_button.onclick = async function(){
            let new_obj
            if (obj == null){
                let data = {}
                for (let f of base_object.fields){
                    if (f != base_object.pk_field){
                        data[f] = document.getElementById(`inp_${f}`).value
                    }
                }
                for (let k in data){
                    if (k in base_object.fk_objects && data[k] == ""){
                        alert("Внешний ключ не может быть пустым. Создайте связанный объект")
                        return throw_pointer.form_view(new_obj)
                    }
                }
                new_obj = await base_object.create_object(data)

            }
            else {
                let data = {}
                for (let f of base_object.fields){
                    if (f != base_object.pk_field){
                        data[f] = document.getElementById(`inp_${f}`).value
                    }
                    else {
                        data[f] = obj[f]
                    }
                }
                for (let k in data){
                    if (k in base_object.fk_objects && data[k] == ""){
                        alert("Внешний ключ не может быть пустым. Создайте связанный объект")
                        return throw_pointer.form_view(obj)
                    }
                }
                new_obj = await base_object.update_object(data)
            }
            await throw_pointer.detail_view(new_obj)
        }

        let list_button = document.querySelector(["button.list"])
        list_button.onclick = async function(){
            await throw_pointer.list_view(throw_pointer.page)
        }
    }
}

function BaseObject(name, fields, pk_field, fk_objects){
    this.pk_field = pk_field
    this.fk_objects = fk_objects
    this.name = name
    this.fields = fields
    this.objects = []
    this.get_object = async function(id){
        try{
            this.object = await sendRequest(`${urls[this.name]}/${id}`, "GET", null)
            return this.object
        } catch (e) {
            alert(e)
        }
    }
    this.get_list = async function(filters= null, page){
        try{
            let order_by = ""
            if (filters != null){
                for (let f of filters) {
                    order_by += `${f},`
                }
                if (order_by.length !=0){
                    order_by = order_by.slice(0, -1)
                }
            }
            console.log(order_by)
            this.objects = await sendRequest(`${urls[this.name]}?limit=${5}&offset=${page*5}&order_by=${order_by}`, "GET", null)
            return this.objects
        } catch (e) {
            alert(e)
        }

    }
    this.update_object = async function(data){
        try{
            this.object = await sendRequest(`${urls[this.name]}`, "PUT", data)
            return this.object
        } catch (e) {
            alert(e)
        }
    }

    this.create_object = async function(data){
        try{
            this.object = await sendRequest(`${urls[this.name]}`, "POST", data)
            return this.object
        } catch (e) {
            alert(e)
        }

    }
    this.delete_object = async function(id){
        try{
            this.object = null
            return await sendRequest(`${urls[this.name]}/${id}`, "DELETE", null)
        } catch (e) {
            alert(e)
        }
    }

    this.get_fkey_object = async function(id, name, many=false){
        if (many){
            return await sendRequest(`${urls[name]}`, "GET", null)
        }
        return await sendRequest(`${urls[name]}/${id}`, "GET", null)
    }

    this.list_html = async function(){
        let html = "<hr>"
        for (let o of this.objects){
            html += `<div class="${name}_card" id="${o[pk_field]}">`
            html += `<button class="retrieve" id="ret_${o[pk_field]}">Подробнее</button>`
            html += `<button class="edit" id="ch_${o[pk_field]}">Изменить</button>`
            html += `<button class="delete" id="del_${o[pk_field]}">Удалить</button>`
            for (let f of this.fields){
                if (f != pk_field){
                    if (f in this.fk_objects){
                        let fk_object = await this.get_fkey_object(o[f], this.fk_objects[f])
                        html += `<p>${f.slice(0, -3)}: ${fk_object.name}</p>`
                    }
                    else {
                        html += `<p>${f}: ${o[f]}</p>`
                    }
                }
            }
            html += `</div>`
        }
        return html
    }

    this.single_view = async function(obj){
        let html = `<div class="${name}_retrieve" id="${obj[pk_field]}">`
        html += `<button class="edit" id="ch_${obj[pk_field]}">Изменить</button>`
        html += `<button class="delete" id="del_${obj[pk_field]}">Удалить</button>`
        html += `<button class="list" id="list_${obj[pk_field]}">К списку</button>`
        for (let f of this.fields){
            if (f != pk_field){
                if (f in this.fk_objects){
                    let fk_object = await this.get_fkey_object(obj[f], this.fk_objects[f])
                    html += `<p>${f.slice(0, -3)}: ${fk_object.name}</p>`
                }
                else {
                    html += `<p>${f}: ${obj[f]}</p>`
                }
            }
        }
        html += `</div>`
        return html
    }

    this.object_form_html = async function(obj){
        let html = ""
        if (obj == null){
            html += `<div class="${name}_create">`
            html += `<button class="cancel" id="c_create">Отмена</button>`
            html += `<button class="save" id="save_create">Сохранить</button>`
            html += `<button class="list" id="list_create">К списку</button>`
            for (let f of this.fields){
                if (f != pk_field){
                    if (f in this.fk_objects){
                        let fk_objects = await this.get_fkey_object(null, this.fk_objects[f], true)
                        html += `<p>${f.slice(0, -3)}: <select id="inp_${f}" class="fk_${f.slice(0, -3)}">`
                        for (let opt of fk_objects){
                            html += `<option value="${opt[this.pk_field]}">${opt.name}</option>`
                        }
                        html += `</select></p>`

                    }
                    else {
                        html += `<p>${f}: <input id="inp_${f}" type="text"/></p>`
                    }
                }
            }
            html += `</div>`
        }
        else {
            html += `<div class="${name}_edit">`
            html += `<button class="cancel" id="c_${obj[pk_field]}">Отмена</button>`
            html += `<button class="save" id="save_${obj[pk_field]}">Сохранить</button>`
            html += `<button class="list" id="list_${obj[pk_field]}">К списку</button>`
            for (let f of this.fields){
                if (f != pk_field){
                    if (f in this.fk_objects){
                        let fk_objects = await this.get_fkey_object(null, this.fk_objects[f], true)
                        html += `<p>${f.slice(0, -3)}: <select id="inp_${f}" value="${obj[f]}" class="fk_${f.slice(0, -3)}">`
                        for (let opt of fk_objects){
                            if (opt[this.pk_field] == obj[f]){
                                html += `<option selected value="${opt[this.pk_field]}">${opt.name}</option>`
                            }
                            else{
                                html += `<option value="${opt[this.pk_field]}">${opt.name}</option>`
                            }
                        }
                        html += `</select></p>`
                    }
                    else {
                        html += `<p>${f}: <input id="inp_${f}" value="${obj[f]}" type="text"/></p>`
                    }
                }
            }
            html += `</div>`
        }
        return html
    }
}