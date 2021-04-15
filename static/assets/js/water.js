const app = new Vue({
    delimiters: ['[[', ']]'],
    data() {
        return {
            water_source: undefined,
            is_access_to_water: undefined,
            is_source: undefined,
            is_source_common: undefined,
            is_people_have_house_source: undefined,
            shows: {
                is_access_to_water_true: false,
                is_access_to_water_false: true,
                water_source_5: false,
                water_source_6: false,
                is_water_network_true: false,
                is_source_network_true: false,
                is_source_common_true: false,
                is_people_have_house_source_true: false,
            },
        }
    },
    el: '#form',
    mounted: function () {

    },
    methods: {
        map2Handler() {
            if (this.water_source === '5')
                showSecondMap()
        },
    },
    computed: {
        // waterSource: function () {
        //     return $(`[name="water_source"]:checked`).val()
        // },
    }
})
