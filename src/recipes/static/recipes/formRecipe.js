const counterId = document.querySelector('#counter');

const ingredientsContainer = document.querySelector('.form__field-group-ingredientes-container');
const nameIngredient = document.querySelector('#nameIngredient');
const formDropdownItems = document.querySelector('.form__dropdown-items');
const cantidadVal = document.querySelector('#cantidadVal');
const cantidad = document.querySelector('#cantidad')
const cantidadId = document.querySelector('#cantidadId')
const addIng = document.querySelector('#addIng');

const api = new Api(apiUrl);
const header = new Header(counterId);

const defineInitialIndex = function () {
    const ingredients = ingredientsContainer.querySelectorAll('.form__field-item-ingredient')
    if (ingredients.length === 0) { return 1 }
    const data = Array.from(ingredients).map(item => {
        if (!item.getAttribute('id')) { return 0 }
        if (!item.getAttribute('id').split('_')[1]) { return 0 }
        return Number(item.getAttribute('id').split('_')[1])
    })
    data.sort((a, b) => a-b)
    return data[data.length - 1] + 1
}

function Ingredients() {
    let cur = defineInitialIndex();
    // клик по элементам с сервера
    const dropdown = (e) => {
        if (e.target.classList.contains('form__item-list')) {
            nameIngredient.value = e.target.textContent;
            formDropdownItems.style.display = ''
            cantidadVal.textContent = e.target.getAttribute('data-val');
            cantidadId.value = e.target.getAttribute('data-id');
        }
    };
    // Добавление элемента из инпута
    const addIngredient = (e) => {
        if(cantidadId.value && nameIngredient.value && cantidad.value > 0) {
            const data = getValue();
            const elem = document.createElement('div');
            elem.classList.add('form__field-item-ingredient');
            elem.id = `ing_${cur}`;
            elem.innerHTML = `<span> ${data.name} ${data.value}${data.units}</span> <input type="checkbox" name="recipeingredient_set-{{ forloop.counter0 }}-DELETE" id="id_recipeingredient_set-{{ forloop.counter0 }}-DELETE" class="form__field-item-delete delete__checkbox">
                             <label for="id_recipeingredient_set-{{ forloop.counter0 }}-DELETE"></label>
                             <input id="id_recipeingredient_set-${cur}-title" name="recipeingredient_set-${cur}-title" type="hidden" value="${data.name}">
                             <input id="id_recipeingredient_set-${cur}-amount" name="recipeingredient_set-${cur}-amount" type="hidden" value="${data.value}">
                             <input id="id_recipeingredient_set-${cur}-dimension" name="recipeingredient_set-${cur}-dimension" type="hidden" value="${data.units}">
                             <input id="id_recipeingredient_set-${cur}-ingredient" name="recipeingredient_set-${cur}-ingredient" type="hidden" value="${data.id}">`;
            cur++;

            ingredientsContainer.appendChild(elem);
        }
    };
    // удаление элемента

    const eventDelete = (e) => {
        if(e.target.classList.contains('form__field-item-delete')) {
            const item = e.target.closest('.form__field-item-ingredient');
            item.removeEventListener('change',eventDelete);
            // item.remove()
            item.style.display = "none";
        };
    };
    ingredientsContainer.addEventListener('change', eventDelete);
    // получение данных из инпутов для добавления
    const getValue = (e) => {
        const data = {
            name: nameIngredient.value,
            value: cantidad.value,
            units: cantidadVal.textContent,
            id: cantidadId.value
        };
        clearValue(nameIngredient);
        clearValue(cantidad);
        clearValue(cantidadId);
        return data;
    };
    // очистка инпута
    const clearValue = (input) => {
        input.value = '';
    };
    return {
        clearValue,
        getValue,
        addIngredient,
        dropdown
    }
}

const cbEventInput = (elem) => {
    if(elem.target.value.length == 0) {
        formDropdownItems.style.display = 'none';
        return
    }
    return api.getIngredients(elem.target.value).then( e => {
        if(e.length !== 0 ) {
            const items = e.map( elem => {
                return `<a class="form__item-list" data-id="${elem.pk}" data-val="${elem.dimension}"">${elem.title}</a>`
            }).join(' ')
            formDropdownItems.style.display = 'flex';
            formDropdownItems.innerHTML = items;
        }
    })
    .catch( e => {
        console.log(e)
    })
};

const eventInput = debouncing(cbEventInput, 1000);

// вешаем апи
nameIngredient.addEventListener('input', eventInput);
const ingredients = Ingredients();
// вешаем слушатель на элементы с апи
formDropdownItems.addEventListener('click', ingredients.dropdown);
// вешаем слушатель на кнопку
addIng.addEventListener('click', ingredients.addIngredient);
