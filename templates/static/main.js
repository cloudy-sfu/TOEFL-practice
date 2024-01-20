function bind_search_field(input_id, select_id) {
    let input_tag = document.getElementById(input_id);
    let select_tag = document.getElementById(select_id);
    input_tag.addEventListener('input', function() {
        let filter = input_tag.value.toLowerCase();
        let options = select_tag.options;
        let first_i = null;
        for (let i = 0; i < options.length; i++) {
            let option = options[i];
            let optionText = option.text.toLowerCase();
            if (optionText.includes(filter)) {
                option.style.display = "";
                if (first_i === null) {first_i = i}
            } else {
                option.style.display = "none";
            }
        }
        select_tag.selectedIndex = first_i;
    });
}